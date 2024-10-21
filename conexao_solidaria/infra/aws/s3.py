import boto3
from conexao_solidaria.utils.date import format_date
from conexao_solidaria.core.config import settings


class S3:
    def __init__(self) -> None:
        self.client = boto3.client("s3", region_name=settings.REGION_NAME)

    def get_object_url(self, bucket: str, key: str) -> str:
        """Retorna a URL do objeto."""
        return f"https://{bucket}.s3.amazonaws.com/{key.replace(' ', '+')}"

    def get_object_metadata(self, bucket: str, key: str) -> dict:
        """Obtém metadados do objeto."""
        return self.client.head_object(Bucket=bucket, Key=key)

    def get_created_timestamp(self, bucket: str, key: str) -> str:
        """Retorna a data da última modificação do objeto."""
        metadata = self.get_object_metadata(bucket, key)
        return format_date(metadata["LastModified"])

    def put_objetct(self, bucket: str, body: bytes, key: str, contentType: str) -> None:
        """Armazena o arquivo no bucket."""
        self.client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType=contentType
        )

    def get_object(self, bucket: str, key: str) -> bytes:
        """Obtém o objeto do S3 e retorna seu conteúdo em bytes."""
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()
