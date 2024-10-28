from typing import Dict, List, Union

import requests


def get_endpoint_data(endpoint: str) -> Union[Dict, List[Dict], None]:
    """
    Retrieves JSON data from the specified endpoint.
    """
    try:
        response = requests.get(endpoint, timeout=20)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consumir o endpoint: {e}")
        return None
