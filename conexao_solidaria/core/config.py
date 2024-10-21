from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define configurações e variáveis de ambiente que serão usadas no projeto"""

    REGION_NAME: str = ""
    TABLE_NAME: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
