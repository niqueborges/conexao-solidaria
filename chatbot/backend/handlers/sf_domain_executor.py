from aws_lambda_powertools import Logger, Tracer
from infrastructure.engines import LexEngine
from infrastructure.providers import (
    ApiGatewayInstitutionRepository,
    ViaCepProvider,
    RekognitionModerationService,
    PollySpeechService,
)
from domain.adapters.lex_mapper import LexMapper
from domain.services.registration_flow import RegistrationFlow
from domain.services.list_flow import ListFlow
from domain.services.tips_flow import TipsFlow
from domain.services.welcome_flow import WelcomeFlow

logger = Logger()
tracer = Tracer()
lex_engine = LexEngine()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    intent_name = event.get("intent_name")
    slots = event.get("slots", {})
    session_id = event.get("session_id")
    original_message = event.get("original_message")
    
    response_text = ""
    
    if intent_name == "WelcomeIntent":
        flow = WelcomeFlow()
        result = flow.process_welcome(message=original_message, session_id=session_id, lex_engine=lex_engine)
        if isinstance(result, str):
            response_text = result
        else:
            response_text = result.message

    elif intent_name == "RegisterIntent":
        flow = RegistrationFlow(
            repository=ApiGatewayInstitutionRepository(),
            address_provider=ViaCepProvider(),
            moderation_service=RekognitionModerationService(),
            speech_service=PollySpeechService(),
        )
        request = LexMapper.to_registration_request(slots)
        response_text = flow.execute_registration(request)
        
    elif intent_name == "ListRegisteredInstitutionsIntent":
        flow = ListFlow()
        request = LexMapper.to_list_request(slots)
        response_text = flow.execute_list(request)
        
    elif intent_name == "TipsIntent":
        from infrastructure.engines import BedrockEngine
        flow = TipsFlow(engine=BedrockEngine())
        flat_slots = LexMapper.extract_flat_slots(slots)
        tip_type = flat_slots.get("TipType")
        response_text = flow.execute_tips(tip_type)

    lex_engine.clear_session(session_id)

    # Re-pass bot_number to ensure the next state has it
    return {
        "response_message": response_text,
        "session_id": session_id,
        "bot_number": event.get("bot_number", "")
    }
