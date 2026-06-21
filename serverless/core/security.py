from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from utils.build import build_http_response
import os

@lambda_handler_decorator
def verify_origin(handler, event, context):
    """
    Middleware to ensure the request comes from CloudFront.
    CloudFront injects the X-Origin-Verify header.
    """
    # Se for uma chamada local (serverless-offline), pode não ter o header.
    if os.environ.get("IS_OFFLINE") == "true":
        return handler(event, context)

    headers = event.get("headers", {})
    # API Gateway lowercases all headers
    if headers.get("x-origin-verify") != "SECRET-WAF-TOKEN-12345":
        return build_http_response(
            status_code=403, 
            body={"detail": "Forbidden: Direct access to API Gateway is not allowed. Please use CloudFront."}
        )
    return handler(event, context)
