from aws_lambda_powertools import Logger, Tracer
from infrastructure.engines import LexEngine, BedrockEngine
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

class ConversationOrchestrator:
    def __init__(self, lex_engine=None, bedrock_engine=None):
        self.lex = lex_engine or LexEngine()
        self.bedrock = bedrock_engine or BedrockEngine()

    @tracer.capture_method
    def process_message(self, message: str, session_id: str) -> str:
        # 1. Tenta rotear pelo Lex (barato, regras estruturadas)
        lex_context = self.lex.analyze(message, session_id)
        
        # 2. Roteamento baseado no entendimento
        if lex_context.intent_name == "FallbackIntent":
            logger.info("Lex Fallback acionado. Redirecionando para o BedrockEngine.")
            return self.bedrock.process(message)
            
        if lex_context.intent_name == "WelcomeIntent":
            flow = WelcomeFlow()
            result = flow.process_welcome(message=message, session_id=session_id, lex_engine=self.lex)
            if isinstance(result, str):
                return result
            # Se não retornou string, retornou o novo lex_context mapeado para fulfillment!
            lex_context = result
            
        if lex_context.ready_for_fulfillment:
            logger.info(f"Fulfillment acionado para a intent: {lex_context.intent_name}")
            
            response_text = ""
            if lex_context.intent_name == "RegisterIntent":
                flow = RegistrationFlow(
                    repository=ApiGatewayInstitutionRepository(),
                    address_provider=ViaCepProvider(),
                    moderation_service=RekognitionModerationService(),
                    speech_service=PollySpeechService(),
                )
                request = LexMapper.to_registration_request(lex_context.slots)
                response_text = flow.execute_registration(request)
                
            elif lex_context.intent_name == "ListRegisteredInstitutionsIntent":
                flow = ListFlow()
                request = LexMapper.to_list_request(lex_context.slots)
                response_text = flow.execute_list(request)
                
            elif lex_context.intent_name == "TipsIntent":
                flow = TipsFlow(engine=self.bedrock)
                flat_slots = LexMapper.extract_flat_slots(lex_context.slots)
                tip_type = flat_slots.get("TipType")
                response_text = flow.execute_tips(tip_type)
                
            # Limpa a sessão para garantir que o usuário não fique preso na intent finalizada
            self.lex.clear_session(session_id)
            return response_text
                
        # 3. Retorna a pergunta do Lex (ElicitSlot ou mensagem inicial)
        return lex_context.message
