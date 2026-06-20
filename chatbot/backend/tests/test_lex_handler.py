import pytest
from handlers.lex import lex

def test_lex_register_intent(mocker):
    event = {
        "invocationSource": "DialogCodeHook",
        "sessionState": {
            "intent": {
                "name": "RegisterIntent",
                "state": "InProgress"
            }
        }
    }
    context = mocker.Mock()
    
    # We mock RegisterIntent to avoid executing actual logic and hitting external APIs
    mock_register_intent = mocker.patch('handlers.lex.RegisterIntent')
    mock_instance = mock_register_intent.return_value
    mock_instance.process_dialog_hook.return_value = {"mocked": "response"}
    
    response = lex(event, context)
    
    assert response == {"mocked": "response"}
    mock_instance.process_dialog_hook.assert_called_once()
