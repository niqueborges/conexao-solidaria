import boto3
from utils.date import format_date
from core.config import settings


class S3:
    def __init__(self) -> None:
        self.client = boto3.client("s3", region_name=settings.REGION_NAME)

    def get_object_url(self, bucket: str, key: str) -> str:
        """Returns the object's URL."""
        return f"https://{bucket}.s3.amazonaws.com/{key.replace(' ', '+')}"

    def get_object_metadata(self, bucket: str, key: str) -> dict:
        """Retrieves the object's metadata."""
        return self.client.head_object(Bucket=bucket, Key=key)

    def get_created_timestamp(self, bucket: str, key: str) -> str:
        """Returns the object's last modified date."""
        metadata = self.get_object_metadata(bucket, key)
        return format_date(metadata["LastModified"])

    def put_object(self, bucket: str, body: bytes, key: str, contentType: str) -> None:
        """Stores the file in the bucket."""
        self.client.put_object(
            Bucket=bucket, Key=key, Body=body, ContentType=contentType
        )

    def get_object(self, bucket: str, key: str) -> bytes:
        """Retrieves the object from S3 and returns its content as bytes."""
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()
