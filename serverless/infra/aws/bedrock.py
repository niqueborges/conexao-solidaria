import boto3
from botocore.exceptions import ClientError
from core.config import settings


class Bedrock:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=settings.REGION_NAME)

    def generate_tips(self, user_message: str):
        conversation = [{"role": "user", "content": [{"text": user_message}]}]

        try:
            response = self.client.converse(
                modelId=settings.MODEL_ID,
                messages=conversation,
                inferenceConfig={
                    "maxTokens": 420,
                    "stopSequences": [],
                    "temperature": 0.7,
                    "topP": 0.9,
                },
            )

            response_text = (
                response.get("output", {})
                .get("message", {})
                .get("content", [{}])[0]
                .get("text", "Sem resposta.")
            )
            return {"Dicas": response_text}

        except ClientError as e:
            print(f"Erro ao chamar o modelo Bedrock: {e}")
            return {"Erro": str(e)}
