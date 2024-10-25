from typing import Optional
from pydantic import BaseModel, Field


url_pattern = r"^(http|https):\/\/[^\s$.?#].[^\s]*$"
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class InstitutionIn(BaseModel):
    """Schema for creating a new institution"""

    cnpj: str = Field(max_length=14, description="")
    name: str = Field(description="")
    email: str = Field(
        pattern=email_pattern,
        description="",
    )
    phone_number: str = Field(max_length=11, description="")
    region: str = Field(description="")
    state: str = Field(description="")
    cep: str = Field(max_length=8, description="")
    address_number: int = Field(description="")
    confirmation_audio: str = Field(pattern=url_pattern, description="")
    image: str = Field(pattern=url_pattern, description="")
    about: str = Field(description="")
    site: Optional[str] = Field(default=None, pattern=url_pattern, description="")
