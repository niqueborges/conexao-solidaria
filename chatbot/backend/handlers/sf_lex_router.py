from aws_lambda_powertools import Logger, Tracer
from infrastructure.engines import LexEngine

logger = Logger()
tracer = Tracer()
lex_engine = LexEngine()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    message = event.get("message", "")
    session_id = event.get("session_id", "")

    logger.info(f"Roteando mensagem: {message} para session: {session_id}")

    lex_context = lex_engine.analyze(message, session_id)

    return {
        "intent_name": lex_context.intent_name,
        "slots": lex_context.slots,
        "lex_response_message": lex_context.message,
        "ready_for_fulfillment": lex_context.ready_for_fulfillment,
        "session_id": session_id,
        "original_message": message,
        "bot_number": event.get("bot_number", ""),
    }
