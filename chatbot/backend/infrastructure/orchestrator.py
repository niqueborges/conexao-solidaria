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
            text = message.lower().strip()
            
            # Correção de Roteamento Pós-Menu:
            # Como limpamos a sessão após o "sim", o Lex recebe "1", "2" ou "3" sem contexto.
            # O NLP do Lex acaba mapeando números soltos erroneamente de volta para WelcomeIntent.
            # Aqui, nós interceptamos os números do menu e injetamos a frase correta para o Lex!
            if text in ["1", "2", "3"]:
                menu_map = {
                    "1": "Quero verificar as instituições cadastradas",
                    "2": "Quero cadastrar uma instituição",
                    "3": "Quero dicas de doação"
                }
                logger.info(f"Interceptando opção '{text}' do menu e re-roteando o Lex.")
                # Re-analisa a mensagem com a frase perfeita para o Lex ativar a intent correta
                lex_context = self.lex.analyze(menu_map[text], session_id)
            else:
                import re
                if re.search(r'\b(sim|concordo|ok|aceito|li)\b', text):
                    # Limpa a sessão do Lex para ele não ficar preso no slot FilterBoolean
                    self.lex.clear_session(session_id)
                    return (
                        "Ótimo! Agora que você está ciente dos termos, escolha uma das opções abaixo para continuarmos:\n"
                        "1. Verificar instituições.\n"
                        "2. Cadastrar uma instituição.\n"
                        "3. Pedir dicas.\n"
                        "É só responder com o número da opção que você prefere!"
                    )
                return (
                    "Olá! Seja bem-vindo! Antes de começarmos, dê uma olhada em nossos Termos de Uso "
                    "acessando a aba 'Termos de Uso' no nosso site.\n\n"
                    "Para prosseguirmos, você está ciente e aceita nossos Termos? (Responda 'sim')"
                )
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
