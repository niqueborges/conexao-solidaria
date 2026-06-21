import sys
from unittest.mock import MagicMock
def dummy_decorator(func):
    return func
mock_tracer = MagicMock()
mock_tracer.capture_method = dummy_decorator
mock_tracer.capture_lambda_handler = dummy_decorator
mock_logger = MagicMock()
mock_logger.inject_lambda_context = lambda **kwargs: dummy_decorator
sys.modules['aws_lambda_powertools'] = MagicMock(
    Tracer=MagicMock(return_value=mock_tracer),
    Logger=MagicMock(return_value=mock_logger)
)

from infrastructure.orchestrator import ConversationOrchestrator
from domain.schemas import ConversationContext

class MockLexEngine:
    def __init__(self, context_to_return: ConversationContext):
        self.context_to_return = context_to_return
        self.analyzed_text = None
        
    def analyze(self, text: str, session_id: str) -> ConversationContext:
        self.analyzed_text = text
        return self.context_to_return

class MockBedrockEngine:
    def __init__(self):
        self.processed_prompt = None
        
    def process(self, prompt: str) -> str:
        self.processed_prompt = prompt
        return "Resposta Bedrock"

def test_orchestrator_lex_fallback():
    # Se Lex retornar FallbackIntent, deve usar Bedrock
    lex_mock = MockLexEngine(ConversationContext(
        intent_name="FallbackIntent",
        slots={},
        message="Lex Elicit Slot (ignorado)",
        ready_for_fulfillment=False
    ))
    bedrock_mock = MockBedrockEngine()
    
    orchestrator = ConversationOrchestrator(lex_engine=lex_mock, bedrock_engine=bedrock_mock)
    
    result = orchestrator.process_message("Como doar?", "sess-123")
    
    assert lex_mock.analyzed_text == "Como doar?"
    assert bedrock_mock.processed_prompt == "Como doar?"
    assert result == "Resposta Bedrock"

def test_orchestrator_lex_elicit():
    # Se Lex ainda está no meio de um diálogo (ElicitSlot), retorna a mensagem do Lex
    lex_mock = MockLexEngine(ConversationContext(
        intent_name="RegisterIntent",
        slots={},
        message="Por favor, me informe o CNPJ.",
        ready_for_fulfillment=False
    ))
    bedrock_mock = MockBedrockEngine()
    
    orchestrator = ConversationOrchestrator(lex_engine=lex_mock, bedrock_engine=bedrock_mock)
    
    result = orchestrator.process_message("Quero me registrar", "sess-123")
    
    assert lex_mock.analyzed_text == "Quero me registrar"
    assert bedrock_mock.processed_prompt is None # Não acionou Bedrock
    assert result == "Por favor, me informe o CNPJ."
