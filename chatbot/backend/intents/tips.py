from aws_lambda_powertools import Logger
from utils.responses import LexResponses
from domain.adapters.lex_mapper import LexMapper
from domain.services.tips_flow import TipsFlow

from infrastructure.providers import BedrockEngine

logger = Logger()

class TipsIntent:
    """
    Class responsible for handling events related to the TipsIntent intent.
    """

    def __init__(self, event: dict) -> None:
        self.event = event
        self.flow = TipsFlow(engine=BedrockEngine())

    def process_dialog_hook(self) -> LexResponses:
        slots = self.event["sessionState"]["intent"]["slots"]
        flat_slots = LexMapper.extract_flat_slots(slots)
        
        result = self.flow.validate_step(flat_slots)
        
        if not result.is_valid:
            return LexResponses.elicit_slot(self.event, result.elicit_slot)
            
        return LexResponses.delegate(self.event)

    def process_full_fillment(self) -> LexResponses:
        slots = self.event["sessionState"]["intent"]["slots"]
        flat_slots = LexMapper.extract_flat_slots(slots)
        
        tip_type = flat_slots.get("TipType")
        response_message = self.flow.execute_tips(tip_type)

        response = LexResponses.sent_fulfillment_response(
            self.event, slots, response_message
        )
        logger.info(f"Response : {response}")
        return response
