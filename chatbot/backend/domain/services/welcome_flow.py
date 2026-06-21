from domain.schemas import ValidationResult
from domain.services.validators import DomainValidators

from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

class WelcomeFlow:
    @tracer.capture_method
    def validate_step(self, field_values: dict) -> ValidationResult:
        rules = {
            "FilterBoolean": DomainValidators.validate_boolean_sim_nao,
            "AvailableIntents": DomainValidators.validate_intent_choice,
        }

        for field_name, value in field_values.items():
            if value is None:
                continue
                
            validator = rules.get(field_name)
            if validator and not validator(value):
                return ValidationResult(is_valid=False, elicit_slot=field_name)

        return ValidationResult(is_valid=True)
