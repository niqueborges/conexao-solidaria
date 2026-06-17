import httpx
from django.http import HttpRequest
from typing import Any

import logging

logger = logging.getLogger(__name__)

async def fetch_data(endpoint: str) -> dict[str, Any]:
    """
    Retrieves JSON data from the specified endpoint asynchronously.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, timeout=5.0)
            response.raise_for_status()
    except httpx.RequestError as exc:
        logger.error(f"Erro de conexão ao consumir o endpoint: {exc}")
        return {}
    except httpx.HTTPStatusError as exc:
        logger.error(f"Erro HTTP {exc.response.status_code} ao consumir o endpoint: {exc}")
        return {}

    return response.json()


def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip
