import os
from twilio.rest import Client
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    response_message = event.get("response_message") or event.get("lex_response_message", "")
    to_number = event.get("session_id", "") 
    from_number = event.get("bot_number", "") 
    
    if not response_message:
        logger.warning("No message to send.")
        return {"status": "skipped"}
        
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    
    if not twilio_account_sid or not twilio_auth_token:
        logger.error("Credenciais Twilio ausentes.")
        return {"status": "error", "reason": "missing credentials"}
        
    client = Client(twilio_account_sid, twilio_auth_token)
    
    try:
        client.messages.create(
            body=response_message,
            from_=from_number,
            to=to_number
        )
        logger.info(f"Mensagem enviada via API REST para {to_number}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Erro ao enviar via Twilio: {e}", exc_info=True)
        raise e
