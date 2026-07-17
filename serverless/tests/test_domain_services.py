import pytest
from domain.services.institution import InstitutionService
from infra.schemas.institutions import CreateInstitution, UpdateInstitution
from core.exceptions import InstitutionAlreadyExistsException
from infra.repositories.institution import PynamoDBInstitutionRepository


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
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About us",
        site="http://www.test.com",
    )

    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    response = service.create(data)
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
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About us",
        site="http://www.test.com",
    )

    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    service.create(data)

    with pytest.raises(InstitutionAlreadyExistsException):
        service.create(data)


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
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About us",
        site="http://www.test.com",
    )
    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    service.create(data)

    response = service.get("12345678901234")
    assert response["name"] == "Test Institution"

def test_get_all_institutions():
    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    
    data = CreateInstitution(
        cnpj="99999999999999",
        name="All Institution",
        email="all@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Sul",
        state="RS",
        address="Rua",
        address_number=1,
        city="PoA",
        neighborhood="Centro",
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About",
        site="http://www.test.com",
    )
    service.create(data)
    
    response = service.get_all()
    assert "institutions" in response
    assert len(response["institutions"]) > 0

def test_query_institutions():
    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    
    data = CreateInstitution(
        cnpj="88888888888888",
        name="Query Institution",
        email="query@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Norte",
        state="AM",
        address="Rua",
        address_number=1,
        city="Manaus",
        neighborhood="Centro",
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About",
        site="http://www.test.com",
    )
    service.create(data)
    
    response = service.query(region="Norte", state="AM")
    assert "institutions" in response
    assert len(response["institutions"]) > 0

def test_update_institution():
    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    
    data = CreateInstitution(
        cnpj="77777777777777",
        name="Old Name",
        email="old@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Norte",
        state="AM",
        address="Rua",
        address_number=1,
        city="Manaus",
        neighborhood="Centro",
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About",
        site="http://www.test.com",
    )
    service.create(data)
    
    update_data = UpdateInstitution(name="New Name")
    response = service.update("77777777777777", update_data)
    assert response["name"] == "New Name"

def test_delete_institution():
    repository = PynamoDBInstitutionRepository()
    service = InstitutionService(repository=repository)
    
    data = CreateInstitution(
        cnpj="66666666666666",
        name="Delete Me",
        email="del@test.com",
        phone_number="11999999999",
        cep="00000000",
        region="Norte",
        state="AM",
        address="Rua",
        address_number=1,
        city="Manaus",
        neighborhood="Centro",
        confirmation_audio="http://example.com/audio.mp3",
        image="http://example.com/image.png",
        about="About",
        site="http://www.test.com",
    )
    service.create(data)
    
    result = service.delete("66666666666666")
    assert result is True
