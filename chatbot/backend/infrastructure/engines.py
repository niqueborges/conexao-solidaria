import os
import boto3
from aws_lambda_powertools import Logger, Tracer
from domain.interfaces import ConversationEngine
from domain.schemas import ConversationContext
from infrastructure.api import ApiClient
from infrastructure.aws import AmazonServices

logger = Logger()
tracer = Tracer()

class BedrockEngine(ConversationEngine):
    def __init__(self):
        self.api_client = ApiClient(os.getenv("BASE_URL"))
        self.amazon_services = AmazonServices(self.api_client)

    @tracer.capture_method
    def process(self, prompt: str) -> str:
        data = {"topic": prompt}
        response = self.amazon_services.post_bedrock(data)
        return response.get("suggestion", "Desculpe, não consegui obter uma resposta.")

class LexEngine:
    def __init__(self):
        self.lex_client = boto3.client("lexv2-runtime", region_name=os.getenv("REGION"))
        self.bot_id = os.getenv("BOT_ID")
        self.alias_id = os.getenv("ALIAS_ID")
        self.locale_id = os.getenv("LOCALE_ID")

    @tracer.capture_method
    def analyze(self, text: str, session_id: str) -> ConversationContext:
        try:
            response = self.lex_client.recognize_text(
                botId=self.bot_id,
                botAliasId=self.alias_id,
                localeId=self.locale_id,
                sessionId=session_id,
                text=text,
            )

            # Extrair a mensagem de retorno do Lex
            bot_message = "\n".join(
                msg.get("content", "").replace("#", "\n")
                for msg in response.get("messages", [])
                if msg.get("contentType") == "PlainText"
            )

            # Extrair o estado atual da intenção
            session_state = response.get("sessionState", {})
            intent = session_state.get("intent", {})
            intent_name = intent.get("name")
            slots = intent.get("slots", {})
            state = intent.get("state") # Failed, Fulfilled, InProgress, ReadyForFulfillment
            
            ready_for_fulfillment = (state == "ReadyForFulfillment" or state == "Fulfilled")

            return ConversationContext(
                intent_name=intent_name,
                slots=slots,
                message=bot_message,
                ready_for_fulfillment=ready_for_fulfillment
            )

        except Exception as e:
            logger.error(f"Erro no LexEngine: {e}")
            return ConversationContext(
                intent_name="FallbackIntent",
                slots={},
                message="Erro ao processar a mensagem no Lex.",
                ready_for_fulfillment=False
            )

    def clear_session(self, session_id: str):
        try:
            self.lex_client.delete_session(
                botId=self.bot_id,
                botAliasId=self.alias_id,
                localeId=self.locale_id,
                sessionId=session_id
            )
            logger.info(f"Sessão {session_id} limpa no Lex.")
        except Exception as e:
            logger.error(f"Erro ao limpar sessão no Lex: {e}")
