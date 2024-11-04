import re
import requests


class AddressViaCep:
    """
    Class to handle address-related operations using the ViaCEP API.
    """

    @staticmethod
    def validate_cep_format(cep: str) -> None:
        """
        Validates the CEP format.
        """

        if not re.match(r"^\d{5}-?\d{3}$", cep):
            raise ValueError(f"Invalid CEP format: {cep}")

    @staticmethod
    def consult_cep_api(cep: str) -> dict:
        """
        Consults the ViaCEP API for address information based on the provided
        CEP (Brazilian postal code).
        """
        AddressViaCep.validate_cep_format(cep)

        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=10)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 404:
                raise ValueError(f"CEP not found: {cep}")
            else:
                raise Exception(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to ViaCEP API: {e}") from e

    @staticmethod
    def format_cep_response(address_data: dict) -> str:
        """
        Formats the address data from a CEP (Brazilian postal code) query into
        a readable string.
        """
        logradouro = address_data.get("logradouro", "N/A")
        bairro = address_data.get("bairro", "N/A")
        localidade = address_data.get("localidade", "N/A")
        uf = address_data.get("uf", "N/A")
        cep = address_data.get("cep", "N/A")

        cep_response = (
            f"{logradouro}, Bairro: {bairro}, Cidade: {localidade}, "
            f"UF: {uf}, CEP: {cep}"
        )
        return cep_response
