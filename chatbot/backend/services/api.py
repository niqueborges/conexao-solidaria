import requests


class ApiClient:
    """Class to handle API connections."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def post(self, endpoint: str, data: dict) -> dict:
        """Sends a POST request to the specified endpoint."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=data)

            if response.status_code != 201 and response.status_code != 200:
                raise ValueError(f"Unexpected status code: {response.status_code}.")

            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            raise e
        except Exception as e:
            print(f"Error: {e}")
            raise e
