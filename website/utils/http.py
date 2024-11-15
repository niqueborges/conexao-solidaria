from typing import Any
import requests


def fetch_data(endpoint: str) -> list[dict[str, Any]]:
    """
    Retrieves JSON data from the specified endpoint.
    """
    try:
        response = requests.get(endpoint, timeout=20)
    except requests.exceptions.RequestException as exc:
        print(f"Erro ao consumir o endpoint: {exc}")
        return

    return response.json().get("institutions", [])
