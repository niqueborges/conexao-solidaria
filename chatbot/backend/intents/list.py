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
            return LexResponses.elicit_slot(self.event, result.elicit_slot)
            
        return LexResponses.delegate(self.event)

    def process_full_fillment(self) -> LexResponses:
        """
        Responsible for processing the FulfillmentCodeHook step of the intent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        
        request = LexMapper.to_list_request(slots)
        response_message = self.flow.execute_list(request)

        response = LexResponses.sent_fulfillment_response(
            self.event, slots, response_message
        )
        return response
