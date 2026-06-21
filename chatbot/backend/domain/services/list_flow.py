import os
from aws_lambda_powertools import Logger, Tracer
from domain.schemas import ValidationResult, ListInstitutionRequest
from domain.services.validators import DomainValidators

logger = Logger()
tracer = Tracer()

class ListFlow:
    def __init__(self):
        self.base_url = os.getenv("INSTITUTIONS_BASE_URL")

    @tracer.capture_method
    def validate_step(self, field_values: dict) -> ValidationResult:
        rules = {
            "FilterBoolean": DomainValidators.validate_boolean_sim_nao,
            "FilterType": DomainValidators.validate_filter_type,
            "Region": DomainValidators.validate_region,
            "States": DomainValidators.validate_state,
        }

        for field_name, value in field_values.items():
            if value is None:
                continue
                
            validator = rules.get(field_name)
            if validator and not validator(value):
                return ValidationResult(is_valid=False, elicit_slot=field_name)

        return ValidationResult(is_valid=True)

    @tracer.capture_method
    def execute_list(self, request: ListInstitutionRequest) -> str:
        if request.filter_boolean and request.filter_boolean.lower() == "não":
            return f"Acesse o nosso link para visualizar todas as instituições: {self.base_url}/"
        
        filter_type = request.filter_type
        if filter_type:
            if filter_type.lower() == "estado":
                filter_type = "state"
                state = request.state or ""
                link = f"{self.base_url}/filter/{filter_type.lower()}/{state.lower()}"
            else:
                filter_type = "region"
                region = request.region or ""
                link = f"{self.base_url}/filter/{filter_type.lower()}/{region.lower()}"
            
            return f"Para visualizar por {filter_type} acesse nosso link: {link}"
        
        return f"Acesse o nosso link para visualizar todas as instituições: {self.base_url}/"
