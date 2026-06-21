from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities import parameters
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
    try:
        waf_token = parameters.get_parameter("/conexao-solidaria/waf-token", max_age=300, decrypt=True)
    except Exception as e:
        return build_http_response(status_code=500, body={"error": "WAF token not configured or accessible."})

    if headers.get("x-origin-verify") != waf_token:
        return build_http_response(
            status_code=403, 
            body={"detail": "Forbidden: Direct access to API Gateway is not allowed. Please use CloudFront."}
        )
    return handler(event, context)
