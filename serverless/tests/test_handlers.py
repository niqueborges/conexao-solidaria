import os
import json
from api.v1.handlers.health import health

def test_health_handler():
    os.environ["IS_OFFLINE"] = "true"
    event = {}
    response = health(event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "message" in body
