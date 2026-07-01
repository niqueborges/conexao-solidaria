from domain.schemas import ValidationResult
from domain.services.validators import DomainValidators

from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

class WelcomeFlow:
    @tracer.capture_method
    def process_welcome(self, message: str, session_id: str, lex_engine) -> str:
        text = message.lower().strip()
        
        # Correção de Roteamento Pós-Menu:
        if text in ["1", "2", "3"]:
            menu_map = {
                "1": "Quero verificar as instituições cadastradas",
                "2": "Quero cadastrar uma instituição",
                "3": "Quero dicas de doação"
            }
            logger.info(f"Interceptando opção '{text}' do menu e re-roteando o Lex.")
            lex_engine.clear_session(session_id)
            lex_context = lex_engine.analyze(menu_map[text], session_id)
            return lex_context
            
        import re
        if re.search(r'\b(sim|concordo|ok|aceito|li)\b', text):
            lex_engine.clear_session(session_id)
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

    @tracer.capture_method
    def validate_step(self, field_values: dict) -> ValidationResult:
        filter_boolean = field_values.get("FilterBoolean")
        available_intents = field_values.get("AvailableIntents")
        
        # Enforce required fields with explicit domain messages (overriding Lex prompts)
        if filter_boolean is None:
            return ValidationResult(
                is_valid=False, 
                elicit_slot="FilterBoolean",
                error_message=(
                    "Olá! Seja bem-vindo! Antes de começarmos dê uma olhada em nossos Termos de Uso "
                    "acessando /terms-of-use/ em nosso site.\n\n"
                    "Para prosseguirmos, você está ciente e aceita nossos Termos de Uso? (Sim ou Não)"
                )
            )
            
        if filter_boolean.lower() == "sim" and available_intents is None:
            return ValidationResult(
                is_valid=False,
                elicit_slot="AvailableIntents",
                error_message=(
                    "Ótimo! Agora que você aceitou os termos e condições, escolha uma das opções abaixo para continuarmos:\n"
                    "1. Verificar instituições.\n"
                    "2. Cadastrar uma instituição.\n"
                    "3. Pedir dicas.\n"
                    "É só responder com o número da opção que você prefere!"
                )
            )

        rules = {
            "FilterBoolean": DomainValidators.validate_boolean_sim_nao,
            "AvailableIntents": DomainValidators.validate_intent_choice,
        }

        error_messages = {
            "FilterBoolean": "Por favor, responda apenas com Sim ou Não para aceitar os Termos de Uso.",
            "AvailableIntents": "Opção inválida. Escolha 1, 2 ou 3."
        }

        for field_name, value in field_values.items():
            if value is None:
                continue
                
            validator = rules.get(field_name)
            if validator and not validator(value):
                return ValidationResult(
                    is_valid=False, 
                    elicit_slot=field_name,
                    error_message=error_messages.get(field_name, "Valor inválido.")
                )

        return ValidationResult(is_valid=True)
