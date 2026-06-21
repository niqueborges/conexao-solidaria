from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from utils.build import build_http_response
from domain.services.institution import InstitutionService
from core.exceptions import InstitutionNotFoundException

@lambda_handler_decorator
def require_token(handler, event, context):
    """
    Middleware to require a valid Bearer token for write operations.
    The token must match the institution's token in DynamoDB.
    """
    headers = event.get("headers", {})
    auth_header = headers.get("authorization", "")
    
    if not auth_header.startswith("Bearer "):
        return build_http_response(
            status_code=401,
            body={"detail": "Unauthorized: Missing or invalid Bearer token."}
        )
    
    token = auth_header.split(" ")[1]
    
    # Retrieve cnpj from pathParameters
    path_parameters = event.get("pathParameters") or {}
    cnpj = path_parameters.get("cnpj")
    
    if not cnpj:
        return build_http_response(
            status_code=400,
            body={"detail": "Bad Request: Missing cnpj in path parameters."}
        )
        
    try:
        institution = InstitutionService.get(cnpj=cnpj)
    except InstitutionNotFoundException as exc:
        return build_http_response(status_code=404, body={"detail": exc.message})
        
    if institution.get("token") != token:
        return build_http_response(
            status_code=403,
            body={"detail": "Forbidden: Invalid token for this institution."}
        )
        
    return handler(event, context)
