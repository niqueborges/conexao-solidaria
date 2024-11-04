from utils.responses import LexResponses
from utils.slots import check_slot_filling, get_slot_value


class ListIntent:
    """
    Class responsible for handling events related to the
    ListRegisteredInstitutionsIntent intent.
    """

    validation_rules = {
        "FilterBoolean": r"^(sim|não)$",
        "FilterType": r"^(estado|região)$",
        "Region": r"^(Norte|Nordeste|Centro-Oeste|Sudeste|Sul)$",
        "States": r"^[a-zA-Z]{2}$",
    }

    def __init__(self, event: dict) -> None:
        self.event = event

    def process_dialog_hook(self) -> LexResponses:
        """
        Responsible for processing the DialogCodeHook step of the intent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        return check_slot_filling(slots, self.event, self.__class__.validation_rules)

    def process_full_fillment(self) -> LexResponses:
        """
        Responsible for processing the FulfillmentCodeHook step of the intent.
        """
        slots = self.event["sessionState"]["intent"]["slots"]
        slot_names = [slot_name for slot_name in slots.keys()]
        slot_values = {name: get_slot_value(slots, name) for name in slot_names}

        filter_boolean = slot_values["FilterBoolean"]
        if filter_boolean == "Não":
            response_message = "Todas as instituições"
        else:
            filter_type = slot_values["FilterType"]
            state = slot_values["States"]

            response_message = f"""FilterBoolean: {filter_boolean},
            FilterType: {filter_type}, state {state}"""

        response = LexResponses.sent_fulfillment_response(
            self.event, slots, response_message
        )
        return response
