from infrastructure.orchestrator import ConversationOrchestrator
from infrastructure.s3 import upload_file_to_s3
from utils.decode import decode_body
from utils.content_type import get_content_type
from utils.download_media import download_media_file
from utils.get_twilio_phone import get_twilio_phone_number

from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def twilio(event, context):
    params = decode_body(event)

    from_number = get_twilio_phone_number(params)
    logger.info(f"Número de origem: {from_number}")
    
    # Injetando Correlation ID no meio do request usando from_number como session_id
    logger.set_correlation_id(from_number)

    content_type = get_content_type(params)
    response_message = None

    orchestrator = ConversationOrchestrator()

    if content_type in ["image", "audio"]:
        media_url = params.get("MediaUrl0")
        logger.info(f"URL da mídia ({content_type}): {media_url}")

        try:
            media_content = download_media_file(media_url)
            media_key = upload_file_to_s3(media_content, content_type)
            logger.info(f"Media stored in S3 at: {media_key}")
            response_message = orchestrator.process_message(media_key, from_number)
        except Exception as e:
            logger.error(f"Error processing media: {e}", exc_info=True)
            response_message = (
                "Houve um problema ao processar seu arquivo."
                " Por favor, tente novamente."
            )

    else:
        text_to_translate = params.get("Body", "")
        response_message = orchestrator.process_message(text_to_translate, from_number)
        logger.info(f"Orchestrator response: {response_message}")

    return {"statusCode": 200, "body": response_message}
