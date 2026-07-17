import os
import json
import boto3
from twilio.request_validator import RequestValidator
from utils.decode import decode_body
from utils.content_type import get_content_type
from utils.download_media import download_media_file
from infrastructure.s3 import upload_file_to_s3
from utils.get_twilio_phone import get_twilio_phone_number

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import SQSEvent
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer, idempotent_function
)

logger = Logger()
tracer = Tracer()
sqs_client = boto3.client('sqs')
sf_client = boto3.client('stepfunctions')

persistence_layer = DynamoDBPersistenceLayer(
    table_name=os.environ.get("IDEMPOTENCY_TABLE_NAME", "twilio-idempotency-dev")
)

def validate_twilio_request(event, params):
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    validator = RequestValidator(auth_token)
    
    headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
    signature = headers.get('x-twilio-signature', '')
    
    host = headers.get('host', '')
    request_context = event.get('requestContext', {})
    path = request_context.get('path', event.get('path', ''))
    url = f"https://{host}{path}"
    
    if not validator.validate(url, params, signature):
        logger.warning("Twilio signature validation failed.")
        return False
    return True

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def twilio_webhook(event, context):
    params = decode_body(event)
    
    if not validate_twilio_request(event, params):
        return {"statusCode": 403, "body": "Forbidden"}

    queue_url = os.environ.get("TWILIO_SQS_QUEUE_URL")
    if queue_url:
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(params)
        )
        logger.info("Mensagem enviada para SQS com sucesso.")
    else:
        logger.error("TWILIO_SQS_QUEUE_URL não configurada.")
        return {"statusCode": 500, "body": "Configuration Error"}

    return {"statusCode": 200, "body": ""}


@idempotent_function(data_keyword_argument="message_sid", persistence_store=persistence_layer)
def process_single_message(message_sid: str, params: dict):
    from_number = get_twilio_phone_number(params)
    to_number = params.get("To", "")
    
    logger.info(f"Processando mensagem (Worker). Origem: {from_number}")
    logger.set_correlation_id(from_number)

    state_machine_arn = os.environ.get("STATE_MACHINE_ARN")
    if not state_machine_arn:
        logger.error("STATE_MACHINE_ARN não configurado.")
        return

    content_type = get_content_type(params)
    message_text = params.get("Body", "")

    # Tratamento de Mídia
    if content_type in ["image", "audio"]:
        media_url = params.get("MediaUrl0")
        logger.info(f"URL da mídia ({content_type}): {media_url}")
        try:
            media_content = download_media_file(media_url)
            media_key = upload_file_to_s3(media_content, content_type)
            logger.info(f"Media stored in S3 at: {media_key}")
            message_text = media_key
        except Exception as e:
            logger.error(f"Error processing media: {e}", exc_info=True)
            message_text = "Houve um problema ao baixar a imagem."

    input_payload = {
        "message": message_text,
        "session_id": from_number,
        "bot_number": to_number
    }

    try:
        sf_client.start_execution(
            stateMachineArn=state_machine_arn,
            name=message_sid, # O nome da execução será o ID único da mensagem do Twilio
            input=json.dumps(input_payload)
        )
        logger.info(f"Execução da State Machine iniciada: {message_sid}")
    except Exception as e:
        logger.error(f"Erro ao iniciar Step Functions: {e}", exc_info=True)
        raise e


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def twilio_worker(event, context):
    sqs_event = SQSEvent(event)
    batch_item_failures = []
    
    for record in sqs_event.records:
        try:
            params = json.loads(record.body)
            message_sid = params.get("MessageSid", record.message_id)
            
            process_single_message(
                message_sid=message_sid, 
                params=params
            )
                
        except Exception as e:
            logger.error(f"Falha ao processar registro SQS: {e}", exc_info=True)
            batch_item_failures.append({"itemIdentifier": record.message_id})
            
    return {"batchItemFailures": batch_item_failures}
