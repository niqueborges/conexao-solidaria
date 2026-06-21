from aws_lambda_powertools import Logger, Tracer
from domain.schemas import ValidationResult
from domain.services.validators import DomainValidators
from domain.interfaces import ConversationEngine

logger = Logger()
tracer = Tracer()

class TipsFlow:
    tips_list = [
        "Qual instituição escolher?",
        "Como doar?",
        "Como achar instituições confiáveis?",
        "Qual tipo de instituição doar?",
    ]

    def __init__(self, engine: ConversationEngine):
        self.engine = engine

    @tracer.capture_method
    def validate_step(self, field_values: dict) -> ValidationResult:
        rules = {
            "TipType": DomainValidators.validate_intent_choice,
        }

        for field_name, value in field_values.items():
            if value is None:
                continue
                
            validator = rules.get(field_name)
            if validator and not validator(value):
                return ValidationResult(is_valid=False, elicit_slot=field_name)

        return ValidationResult(is_valid=True)

    @tracer.capture_method
    def execute_tips(self, tip_type: str) -> str:
        if not tip_type or not tip_type.isdigit():
            return "Ocorreu um erro ao tentar obter uma dica."
            
        tip_index = int(tip_type) - 1
        if tip_index < 0 or tip_index >= len(self.tips_list):
            return "Opção de dica inválida."

        prompt = f"""Você é um assistente virtual dedicado a fornecer
        dicas genéricas e úteis sobre o tema doações. Certifique-se de que as
        informações sejam claras, educadas e não contenham conteúdos ofensivos ou
        sensíveis.Não cite nomes de instituições específicas.As informações são para
        o público brasileiro.Mantenha sua resposta objetiva.Evite qualquer tipo
        de linguagem inadequada ou sugestões que não sejam diretamente relacionadas
        ao tema. Aqui está o pedido do usuário: {self.tips_list[tip_index]}.
        A dica deve conter no máximo 100 palavras."""

        try:
            suggestion = self.engine.process(prompt)
            return suggestion
        except Exception as e:
            logger.error(f"Error fetching tip from conversation engine: {e}")
            return "Ocorreu um erro ao tentar obter uma dica."
