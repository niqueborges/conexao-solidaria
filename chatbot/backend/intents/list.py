from utils.responses import LexResponses
from domain.adapters.lex_mapper import LexMapper
from domain.services.list_flow import ListFlow

class ListIntent:
    """
    Class responsible for handling events related to the
    ListRegisteredInstitutionsIntent intent.
    """

    def __init__(self, event: dict) -> None:
        self.event = event
        self.flow = ListFlow()

    def process_dialog_hook(self) -> LexResponses:
        """
        Responsible for processing the DialogCodeHook step of the intent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        flat_slots = LexMapper.extract_flat_slots(slots)
        
        result = self.flow.validate_step(flat_slots)
        
        if not result.is_valid:
            return LexResponses.elicit_slot(self.event, result.elicit_slot, result.error_message)
            
        if result.is_ready_for_fulfillment:
            # Pula os slots restantes e fecha a intenção
            return {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {
                        "name": self.event["sessionState"]["intent"]["name"],
                        "state": "Fulfilled",
                        "slots": self.event["sessionState"]["intent"]["slots"],
                    },
                }
            }
            
        return LexResponses.delegate(self.event)
