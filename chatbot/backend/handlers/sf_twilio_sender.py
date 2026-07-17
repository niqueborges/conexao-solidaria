import os
from twilio.rest import Client
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters

logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    response_message = event.get("response_message") or event.get(
        "lex_response_message", ""
    )
    to_number = event.get("session_id", "")
    from_number = event.get("bot_number", "")

    if not response_message:
        logger.warning("No message to send.")
        return {"status": "skipped"}

    try:
        secret = parameters.get_secret("conexao-solidaria/twilio", transform="json")
        twilio_account_sid = secret.get("TWILIO_ACCOUNT_SID")
        twilio_auth_token = secret.get("TWILIO_AUTH_TOKEN")
    except Exception as e:
        logger.error(f"Erro ao obter segredo: {e}")
        twilio_account_sid = None
        twilio_auth_token = None

    if not twilio_account_sid or not twilio_auth_token:
        logger.error("Credenciais Twilio ausentes.")
        return {"status": "error", "reason": "missing credentials"}

    client = Client(twilio_account_sid, twilio_auth_token)

    try:
        client.messages.create(body=response_message, from_=from_number, to=to_number)
        logger.info(f"Mensagem enviada via API REST para {to_number}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Erro ao enviar via Twilio: {e}", exc_info=True)
        raise e
