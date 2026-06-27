from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidationResult:
    is_valid: bool
    invalid_field: Optional[str] = None
    error_message: Optional[str] = None
    elicit_slot: Optional[str] = None
    updated_fields: Optional[dict] = None
    is_ready_for_fulfillment: bool = False

@dataclass
class RegistrationRequest:
    cnpj: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    region: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    cep: Optional[str] = None
    address_number: Optional[str] = None
    description: Optional[str] = None
    site: Optional[str] = None
    image_path: Optional[str] = None

@dataclass
class ListInstitutionRequest:
    filter_boolean: Optional[str] = None
    filter_type: Optional[str] = None
    region: Optional[str] = None
    state: Optional[str] = None

@dataclass
class ConversationContext:
    intent_name: Optional[str]
    slots: dict
    message: str
    ready_for_fulfillment: bool
