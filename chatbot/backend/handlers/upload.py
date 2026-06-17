import os
import json
import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()
s3_client = boto3.client("s3")

@logger.inject_lambda_context
def get_upload_url(event, context):
    """
    Generates a presigned S3 URL for the frontend to upload images directly.
    Expects JSON body: { "session_id": "...", "content_type": "image/jpeg" }
    """
    try:
        bucket_name = os.environ.get("S3_BUCKET_NAME")
        
        body_str = event.get("body")
        if not body_str:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing body"})}
            
        body = json.loads(body_str)
        session_id = body.get("session_id")
        content_type = body.get("content_type", "image/jpeg")
        
        if not session_id:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing session_id"})}
            
        key = f"{session_id}-image.jpg"
        
        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket_name,
                "Key": key,
                "ContentType": content_type
            },
            ExpiresIn=3600
        )
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "url": url,
                "key": key
            })
        }
    except Exception as e:
        logger.error(f"Error generating presigned url: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
