from aws_lambda_powertools import Logger
from utils.responses import LexResponses
from domain.adapters.lex_mapper import LexMapper
from domain.services.registration_flow import RegistrationFlow
from utils.slots import update_multiple_slot_values

from infrastructure.providers import (
    ApiGatewayInstitutionRepository,
    ViaCepProvider,
    RekognitionModerationService,
    PollySpeechService,
)

logger = Logger()

class RegisterIntent:
    """
    Class responsible for handling events related to the RegisterIntent intent.
    Acting as an Adapter to the Domain Services.
    """

    def __init__(self, event: dict) -> None:
        self.event = event
        self.flow = RegistrationFlow(
            repository=ApiGatewayInstitutionRepository(),
            address_provider=ViaCepProvider(),
            moderation_service=RekognitionModerationService(),
            speech_service=PollySpeechService(),
        )

    def process_dialog_hook(self) -> LexResponses:
        """
        Responsible for processing the DialogCodeHook step of the RegisterIntent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        flat_slots = LexMapper.extract_flat_slots(slots)
        
        result = self.flow.validate_step(flat_slots)
        
        if result.updated_fields:
            update_multiple_slot_values(self.event, result.updated_fields)

        if not result.is_valid:
            return LexResponses.elicit_slot(self.event, result.elicit_slot, result.error_message)
            
        return LexResponses.delegate(self.event)


