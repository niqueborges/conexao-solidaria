class LexResponses:
    """
    A class to format responses for Amazon Lex.
    """

    @staticmethod
    def sent_fulfillment_response(
        event: dict, slots: dict, response_message: str
    ) -> dict:
        """
        Sends a response to Amazon Lex when all slots are fulfilled.
        """

        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": event["sessionState"]["intent"]["name"],
                    "state": "Fulfilled",
                    "slots": slots,
                },
            },
            "messages": [{"contentType": "PlainText", "content": response_message}],
        }

    @staticmethod
    def elicit_slot(event, slot_to_elicit):
        """
        Sends a response to Amazon Lex to request a specific slot from the user.
        """
        response = {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": slot_to_elicit},
                "intent": event["sessionState"]["intent"],
            }
        }
        return response

    @staticmethod
    def delegate(event):
        """
        Sends a response to Amazon Lex to delegate the conversation.
        """
        return {
            "sessionState": {
                "dialogAction": {"type": "Delegate"},
                "intent": event["sessionState"]["intent"],
            }
        }
