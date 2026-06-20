import pytest
from domain.services.institution import InstitutionService
from infra.schemas.institutions import CreateInstitution
from core.exceptions import InstitutionAlreadyExistsException

def test_create_institution_success():
    data = CreateInstitution(
        cnpj="12345678901234",
        name="Test Institution",
        email="test@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Sudeste",
        state="SP",
        address="Rua Teste",
        address_number=123,
        city="São Paulo",
        neighborhood="Centro",
        confirmation_audio="audio.mp3",
        image="image.png",
        about="About us",
        site="www.test.com"
    )
    
    response = InstitutionService.create(data)
    assert response["cnpj"] == "12345678901234"
    assert response["name"] == "Test Institution"
    assert "id" in response
    assert "token" in response

def test_create_institution_already_exists():
    data = CreateInstitution(
        cnpj="12345678901234",
        name="Test Institution",
        email="test@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Sudeste",
        state="SP",
        address="Rua Teste",
        address_number=123,
        city="São Paulo",
        neighborhood="Centro",
        confirmation_audio="audio.mp3",
        image="image.png",
        about="About us",
        site="www.test.com"
    )
    
    InstitutionService.create(data)
    
    with pytest.raises(InstitutionAlreadyExistsException):
        InstitutionService.create(data)

def test_get_institution_success():
    data = CreateInstitution(
        cnpj="12345678901234",
        name="Test Institution",
        email="test@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Sudeste",
        state="SP",
        address="Rua Teste",
        address_number=123,
        city="São Paulo",
        neighborhood="Centro",
        confirmation_audio="audio.mp3",
        image="image.png",
        about="About us",
        site="www.test.com"
    )
    InstitutionService.create(data)
    
    response = InstitutionService.get("12345678901234")
    assert response["name"] == "Test Institution"
