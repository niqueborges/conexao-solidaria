import json
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools import Logger

logger = Logger()

def get_twilio_credentials() -> tuple[str, str]:
    """
    Fetches Twilio credentials from AWS Secrets Manager.
    Returns:
        tuple: (account_sid, auth_token)
    Raises:
        RuntimeError: Fail-fast if the secret cannot be retrieved or is malformed.
    """
    secret_name = "conexao-solidaria/twilio"
    
    try:
        # Fetching with 60 seconds cache
        secret_string = parameters.get_secret(secret_name, max_age=60)
        secret_dict = json.loads(secret_string)
        
        account_sid = secret_dict.get("ACCOUNT_SID")
        auth_token = secret_dict.get("AUTH_TOKEN")
        
        if not account_sid or not auth_token:
            raise ValueError("ACCOUNT_SID or AUTH_TOKEN missing in the secret payload.")
            
        return account_sid, auth_token

    except Exception as e:
        logger.error(
            "Failed to retrieve Twilio credentials from Secrets Manager. "
            f"SecretName: {secret_name}. Error: {str(e)}",
            exc_info=True
        )
        # Fail-fast: Stop execution immediately
        raise RuntimeError(f"Critical Infrastructure Error: Unable to load {secret_name}") from e
