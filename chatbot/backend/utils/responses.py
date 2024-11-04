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
