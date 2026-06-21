from utils.build import build_http_response

from core.security import verify_origin

@verify_origin
def health(event, context):
    return build_http_response(
        status_code=200,
        body={
            "message": "Go Serverless v4.0!",
        },
    )
