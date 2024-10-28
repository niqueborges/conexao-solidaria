import boto3
from core.config import settings


class ImageModerationProcessor:
    def __init__(self, region_name: str = "us-east-1") -> None:
        """Initializes the Rekognition client with the specified region."""
        self.rekognition_client = boto3.client(
            "rekognition", region_name=settings.REGION_NAME
        )

    def detect_moderation_labels(
        self, bucket_name: str, image_key: str, min_confidence: int = 75
    ) -> dict:
        """Detects moderation labels in an image stored in S3."""
        try:
            response = self.rekognition_client.detect_moderation_labels(
                Image={"S3Object": {"Bucket": bucket_name, "Name": image_key}},
                MinConfidence=min_confidence,
            )
            return response.get("ModerationLabels", [])
        except Exception as e:
            return {"error": str(e)}
