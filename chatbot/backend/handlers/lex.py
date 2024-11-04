from intents.list import ListIntent
from intents.register import RegisterIntent
from intents.tips import TipsIntent
from utils.responses import LexResponses


def lex(event, context):
    """
    Main handler for processing the backend of the Lex chatbot.
    """
    intent_name = event["sessionState"]["intent"]["name"]
    invocation_source = event["invocationSource"]

    intent = None

    if intent_name == "RegisterIntent":
        intent = RegisterIntent(event)
    elif intent_name == "ListRegisteredInstitutionsIntent":
        intent = ListIntent(event)
    elif intent_name == "TipsIntent":
        intent = TipsIntent(event)

    if intent is None:
        return LexResponses.delegate(event)

    if invocation_source == "DialogCodeHook":
        response = intent.process_dialog_hook()
        return response
    if invocation_source == "FulfillmentCodeHook":
        response = intent.process_full_fillment()
        return response
