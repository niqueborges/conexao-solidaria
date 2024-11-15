import requests
from django.http import HttpRequest
from typing import Any


def fetch_data(endpoint: HttpRequest) -> list[dict[str, Any]]:
    """
    Retrieves JSON data from the specified endpoint.
    """
    try:
        response = requests.get(endpoint, timeout=20)
    except requests.exceptions.RequestException as exc:
        print(f"Erro ao consumir o endpoint: {exc}")
        return

    return response.json().get("institutions", [])


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip
