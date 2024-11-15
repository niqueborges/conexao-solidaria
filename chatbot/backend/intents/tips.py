import os

from services.api import ApiClient
from services.aws import AmazonServices
from utils.slots import get_slot_value, check_slot_filling
from utils.responses import LexResponses


class TipsIntent:
    """
    Class responsible for handling events related to the TipsIntent intent.
    """

    validation_rules = {"TipType": r"^[1-4]$"}

    tips = [
        "Qual instituição escolher?",
        "Como doar?",
        "Como achar instituições confiáveis?",
        "Qual tipo de instituição doar?",
    ]

    def __init__(self, event: dict) -> None:
        self.event = event

    def process_dialog_hook(self) -> LexResponses:
        slots = self.event["sessionState"]["intent"]["slots"]
        return check_slot_filling(slots, self.event, self.__class__.validation_rules)

    def process_full_fillment(self) -> LexResponses:
        slots = self.event["sessionState"]["intent"]["slots"]
        print(f"Slots : {slots}")
        slot_names = [slot_name for slot_name in slots.keys()]
        slot_values = {name: get_slot_value(slots, name) for name in slot_names}

        prompt = slot_values["TipType"]
        print(prompt)
        data = {"topic": self.__class__.tips[int(prompt) - 1]}

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
