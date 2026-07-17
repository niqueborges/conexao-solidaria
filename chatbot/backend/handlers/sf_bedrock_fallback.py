from aws_lambda_powertools import Logger, Tracer
from infrastructure.engines import BedrockEngine

logger = Logger()
tracer = Tracer()
bedrock = BedrockEngine()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    message = event.get("original_message", "")
    session_id = event.get("session_id", "")

    logger.info("Executando fallback no Bedrock.")
    response = bedrock.process(message)

    return {
        "response_message": response,
        "session_id": session_id,
        "bot_number": event.get("bot_number", ""),
    }
