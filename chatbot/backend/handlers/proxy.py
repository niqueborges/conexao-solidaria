import os
import json
import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()
lex_client = boto3.client("lexv2-runtime")

@logger.inject_lambda_context
def web_proxy(event, context):
    """
    Proxies chat messages from the frontend to Amazon Lex.
    Expects JSON body: { "message": "...", "session_id": "..." }
    """
    try:
        body_str = event.get("body")
        if not body_str:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing body"})}
            
        body = json.loads(body_str)
        message = body.get("message", "").strip()
        session_id = body.get("session_id")
        
        if not session_id or not message:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing session_id or message"})}
            
        bot_id = os.environ.get("BOT_ID")
        bot_alias_id = os.environ.get("ALIAS_ID")
        locale_id = os.environ.get("LOCALE_ID")
        
        lex_input = {
            "botId": bot_id,
            "botAliasId": bot_alias_id,
            "localeId": locale_id,
            "sessionId": session_id,
            "text": message,
        }
        
        response = lex_client.recognize_text(**lex_input)
        messages = response.get("messages", [])
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"lex": messages, "user": message})
        }
    except ClientError as exc:
        logger.error(f"AWS Error: {exc}")
        return {"statusCode": 500, "body": json.dumps({"error": str(exc), "user": message})}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
