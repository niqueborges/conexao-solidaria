import sys
from unittest.mock import MagicMock


def dummy_decorator(func):
    return func


mock_tracer = MagicMock()
mock_tracer.capture_method = dummy_decorator
mock_tracer.capture_lambda_handler = dummy_decorator


class MockLogger:
    def __init__(self, *args, **kwargs):
        pass

    def inject_lambda_context(self, *args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return args[0]
        return dummy_decorator

    def info(self, *args):
        pass

    def error(self, *args):
        pass

    def warning(self, *args):
        pass

    def set_correlation_id(self, *args):
        pass


sys.modules["aws_lambda_powertools"] = MagicMock(
    Tracer=MagicMock(return_value=mock_tracer), Logger=MockLogger
)

from handlers.sf_lex_router import handler as lex_handler
from handlers.sf_bedrock_fallback import handler as bedrock_handler
from domain.schemas import ConversationContext


class MockLexEngine:
    def __init__(self, context_to_return: ConversationContext):
        self.context_to_return = context_to_return

    def analyze(self, text: str, session_id: str) -> ConversationContext:
        return self.context_to_return


def test_sf_lex_router(monkeypatch):
    from handlers import sf_lex_router

    lex_mock = MockLexEngine(
        ConversationContext(
            intent_name="FallbackIntent",
            slots={},
            message="Fallback via Lex",
            ready_for_fulfillment=False,
        )
    )
    monkeypatch.setattr(sf_lex_router, "lex_engine", lex_mock)

    event = {"message": "Como ajudar?", "session_id": "sess-123", "bot_number": "bot-1"}
    result = lex_handler(event, None)

    assert result["intent_name"] == "FallbackIntent"
    assert result["lex_response_message"] == "Fallback via Lex"
    assert result["bot_number"] == "bot-1"


class MockBedrockEngine:
    def process(self, prompt: str) -> str:
        return "Resposta Bedrock"


def test_sf_bedrock_fallback(monkeypatch):
    from handlers import sf_bedrock_fallback

    bedrock_mock = MockBedrockEngine()
    monkeypatch.setattr(sf_bedrock_fallback, "bedrock", bedrock_mock)

    event = {
        "original_message": "Como ajudar?",
        "session_id": "sess-123",
        "bot_number": "bot-1",
    }
    result = bedrock_handler(event, None)

    assert result["response_message"] == "Resposta Bedrock"
    assert result["session_id"] == "sess-123"
    assert result["bot_number"] == "bot-1"
