import pytest
from typing import Optional, Tuple
from unittest.mock import patch, MagicMock

# Mock powertools early to avoid aws_xray_sdk import errors
import sys
def dummy_decorator(func):
    return func

mock_tracer = MagicMock()
mock_tracer.capture_method = dummy_decorator
mock_tracer.capture_lambda_handler = dummy_decorator

mock_logger = MagicMock()
mock_logger.inject_lambda_context = lambda **kwargs: dummy_decorator

sys.modules['aws_lambda_powertools'] = MagicMock(
    Tracer=MagicMock(return_value=mock_tracer),
    Logger=MagicMock(return_value=mock_logger)
)
from domain.services.validators import DomainValidators
from domain.services.registration_flow import RegistrationFlow
from domain.services.list_flow import ListFlow
from domain.services.tips_flow import TipsFlow
from domain.schemas import RegistrationRequest, ListInstitutionRequest
from domain.interfaces import InstitutionRepository, AddressProvider, ImageModerationService, SpeechService, ConversationEngine

class MockInstitutionRepository(InstitutionRepository):
    def __init__(self):
        self.created_data = None
        
    def create(self, institution_data: dict) -> None:
        self.created_data = institution_data

class MockAddressProvider(AddressProvider):
    def get_address(self, cep: str) -> Optional[Tuple[str, str, str, str, str]]:
        if cep == "00000000":
            return None
        return ("Rua Mock", "Bairro Mock", "Mock City", "MS", "Centro-Oeste")

class MockImageModerationService(ImageModerationService):
    def is_safe(self, image_path: str) -> bool:
        return "safe" in image_path

class MockSpeechService(SpeechService):
    def generate_audio_url(self, text: str) -> str:
        return "https://mock-s3-bucket.s3.amazonaws.com/mock_audio.mp3"

class MockConversationEngine(ConversationEngine):
    def process(self, prompt: str) -> str:
        return "Aqui está sua dica gerada por IA (Mock)."


def test_valid_cnpj():
    assert DomainValidators.validate_cnpj("12345678901234") is True

def test_invalid_cnpj():
    assert DomainValidators.validate_cnpj("1234") is False
    assert DomainValidators.validate_cnpj("123456789012345") is False
    assert DomainValidators.validate_cnpj("abcd5678901234") is False

def test_registration_invalid_email():
    flow = RegistrationFlow(
        MockInstitutionRepository(),
        MockAddressProvider(),
        MockImageModerationService(),
        MockSpeechService()
    )
    result = flow.validate_step({"InstitutionEmail": "invalid-email"})
    assert result.is_valid is False
    assert result.elicit_slot == "InstitutionEmail"

def test_registration_success():
    repo = MockInstitutionRepository()
    flow = RegistrationFlow(
        repo,
        MockAddressProvider(),
        MockImageModerationService(),
        MockSpeechService()
    )
    
    request = RegistrationRequest(
        cnpj="12345678901234",
        name="ONG Teste",
        email="contato@ong.com"
    )
    
    response = flow.execute_registration(request)
    
    assert "Cadastro da instituição realizado com sucesso" in response
    assert "https://mock-s3-bucket.s3.amazonaws.com/mock_audio.mp3" in response
    
    # Ensure domain layer called the repository correctly
    assert repo.created_data is not None
    assert repo.created_data["cnpj"] == "12345678901234"
    assert repo.created_data["name"] == "ONG Teste"
    assert repo.created_data["confirmation_audio"] == "https://mock-s3-bucket.s3.amazonaws.com/mock_audio.mp3"

def test_list_by_region():
    flow = ListFlow()
    flow.base_url = "https://api.example.com"
    
    request = ListInstitutionRequest(
        filter_type="região",
        region="Sudeste"
    )
    
    response = flow.execute_list(request)
    assert "https://api.example.com/filter/region/sudeste" in response

def test_tips_flow():
    engine = MockConversationEngine()
    flow = TipsFlow(engine)
    
    response = flow.execute_tips("1") # 1 = Qual instituição escolher?
    
    assert response == "Aqui está sua dica gerada por IA (Mock)."
