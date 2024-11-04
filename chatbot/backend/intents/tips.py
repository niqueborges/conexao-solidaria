import os

from services.api import ApiClient
from services.aws import AmazonServices
from utils.slots import get_slot_value
from utils.responses import LexResponses


class TipsIntent:
    """
    Class responsible for handling events related to the TipsIntent intent.
    """

    def __init__(self, event: dict) -> None:
        self.event = event

    def process_dialog_hook(self) -> LexResponses:
        pass

    def process_full_fillment(self) -> LexResponses:
        slots = self.event["sessionState"]["intent"]["slots"]
        print(f"Slots : {slots}")
        slot_names = [slot_name for slot_name in slots.keys()]
        slot_values = {name: get_slot_value(slots, name) for name in slot_names}

        prompt = slot_values["TipType"]
        print(prompt)
        data = {"topic": slot_values["TipType"]}

        api_client = ApiClient(os.getenv("BASE_URL"))
        amazon_service = AmazonServices(api_client)

        try:
            response = amazon_service.post_bedrock(data)
            print(response)
            response_message = response["suggestion"]
        except Exception as e:
            print(e)
            response_message = "Ocorreu um erro ao tentar obter uma dica."

        response = LexResponses.sent_fulfillment_response(
            self.event, slots, response_message
        )
        print(f"Response : {response}")
        return response
