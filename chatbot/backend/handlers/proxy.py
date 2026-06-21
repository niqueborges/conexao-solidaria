import os
import json
import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError
from infrastructure.orchestrator import ConversationOrchestrator

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
            
        orchestrator = ConversationOrchestrator()
        response_text = orchestrator.process_message(message, session_id)
        
        # O frontend espera um array de mensagens no formato do Lex
        messages = [{"contentType": "PlainText", "content": response_text}]
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"lex": messages, "user": message})
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
