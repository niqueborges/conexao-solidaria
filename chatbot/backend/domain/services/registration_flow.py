from aws_lambda_powertools import Logger, Tracer
from domain.schemas import ValidationResult, RegistrationRequest
from domain.services.validators import DomainValidators
from domain.interfaces import InstitutionRepository, AddressProvider, ImageModerationService, SpeechService

logger = Logger()
tracer = Tracer()

class RegistrationFlow:
    def __init__(
        self,
        repository: InstitutionRepository,
        address_provider: AddressProvider,
        moderation_service: ImageModerationService,
        speech_service: SpeechService,
    ):
        self.repository = repository
        self.address_provider = address_provider
        self.moderation_service = moderation_service
        self.speech_service = speech_service

    @tracer.capture_method
    def validate_step(self, field_values: dict) -> ValidationResult:
        # 1. Regex Validation
        rules = {
            "CNPJ": DomainValidators.validate_cnpj,
            "InstitutionName": DomainValidators.validate_name,
            "InstitutionEmail": DomainValidators.validate_email,
            "InstitutionPhone": DomainValidators.validate_phone,
            "InstitutionAddressNumber": DomainValidators.validate_address_number,
            "InstitutionSite": DomainValidators.validate_site,
            "InstitutionCep": DomainValidators.validate_cep,
            "InstitutionDescription": DomainValidators.validate_description,
        }

        for field_name, value in field_values.items():
            if value is None:
                continue
                
            # Normalização Automática
            if field_name in ["CNPJ", "InstitutionCep", "InstitutionPhone"]:
                value = re.sub(r"\D", "", value)
                field_values[field_name] = value
                if updated_fields is None:
                    updated_fields = {}
                updated_fields[field_name] = value

            if field_name == "InstitutionSite":
                if not value.startswith(("http://", "https://")):
                    value = f"https://{value}"
                field_values[field_name] = value
                if updated_fields is None:
                    updated_fields = {}
                updated_fields[field_name] = value

            validator = rules.get(field_name)
            if validator and not validator(value):
                return ValidationResult(is_valid=False, elicit_slot=field_name, updated_fields=updated_fields)

            # 2. Image Moderation Validation
            if field_name == "ImagePath":
                if value.strip().lower() not in ["não", "nao", "no"]:
                    is_safe = self.moderation_service.is_safe(value)
                    if not is_safe:
                        return ValidationResult(is_valid=False, elicit_slot=field_name)

        # 3. Address Lookup & Enrichment
        updated_fields = None
        cep = field_values.get("InstitutionCep")
        if cep and field_values.get("InstitutionState") is None:
            address_data = self.address_provider.get_address(cep)
            
            if address_data:
                street, neighborhood, city, state, region = address_data
                updated_fields = {
                    "InstitutionState": state,
                    "InstitutionCity": city,
                    "InstitutionNeighborhood": neighborhood,
                    "InstitutionAddress": street,
                    "InstitutionRegion": region,
                }
                field_values.update(updated_fields)
            else:
                return ValidationResult(is_valid=False, elicit_slot="InstitutionCep")

        # 4. Enforce Elicitation Order
        order = [
            "CNPJ",
            "InstitutionCep",
            "InstitutionAddressNumber",
            "InstitutionName",
            "InstitutionEmail",
            "InstitutionPhone",
            "InstitutionSite",
            "InstitutionDescription",
            "ImagePath"
        ]
        for slot in order:
            if field_values.get(slot) is None:
                return ValidationResult(is_valid=False, elicit_slot=slot, updated_fields=updated_fields)

        return ValidationResult(is_valid=True, updated_fields=updated_fields)

    @tracer.capture_method
    def execute_registration(self, request: RegistrationRequest) -> str:
        try:
            response_message = (
                "Cadastro da instituição realizado com sucesso! "
                "Ele estará disponível assim que aprovado. "
                "Agradecemos pelo seu registro."
            )

            confirmation_audio_url = self.speech_service.generate_audio_url(response_message)

            institution_data = {
                "cnpj": request.cnpj,
                "name": request.name,
                "email": request.email,
                "phone_number": request.phone_number,
                "region": request.region,
                "state": request.state,
                "address": request.address,
                "city": request.city,
                "neighborhood": request.neighborhood,
                "cep": request.cep,
                "address_number": request.address_number,
                "confirmation_audio": confirmation_audio_url,
                "description": request.description,
                "site": request.site,
                "image_path": request.image_path,
            }

            self.repository.create(institution_data)

            response_message += (
                f"Para ouvir a resposta em áudio clique no link : "
                f"{confirmation_audio_url}"
            )
            return response_message

        except Exception as e:
            logger.error(f"Erro ao criar instituição: {e}")
            return "Ocorreu um erro ao cadastrar a sua instituição. Tente novamente mais tarde."
