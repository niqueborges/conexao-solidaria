from utils.responses import LexResponses
from domain.adapters.lex_mapper import LexMapper
from domain.services.welcome_flow import WelcomeFlow

class WelcomeIntent:
    """Class responsible for processing the WelcomeIntent"""

    def __init__(self, event: dict) -> None:
        self.event = event
        self.flow = WelcomeFlow()

    def process_dialog_hook(self) -> LexResponses:
        slots = self.event["sessionState"]["intent"]["slots"]
        flat_slots = LexMapper.extract_flat_slots(slots)
        
        result = self.flow.validate_step(flat_slots)
        
        if not result.is_valid:
            return LexResponses.elicit_slot(self.event, result.elicit_slot, result.error_message)
            
        return LexResponses.delegate(self.event)
