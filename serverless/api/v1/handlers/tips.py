import json
from infra.aws.bedrock import Bedrock
from utils.build import build_http_response


def tips(event, context):
    bedrock_instance = Bedrock()

    body = json.loads(event.get("body", "{}"))
    print(body)
    user_message = body.get("user_message")
    print(user_message)
    response = bedrock_instance.generate_tips(user_message=user_message)

    return build_http_response(status_code=200, body=response)
