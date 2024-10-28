import boto3


class ImageModerationProcessor:
    def __init__(self, region_name: str = "us-east-1") -> None:
        """Initializes the Rekognition client with the specified region."""
        self.rekognition_client = boto3.client("rekognition", region_name=region_name)

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

    def process_image(self, bucket_name: str, image_key: str) -> dict:
        """Processes an image and checks for inappropriate content."""
        labels = self.detect_moderation_labels(bucket_name, image_key)

        """Returns only if there is inappropriate content"""
        if labels:
            result = {
                "message": "The image contains inappropriate content.",
                "labels": [],
            }
            for label in labels:
                result["labels"].append(
                    {"name": label["Name"], "confidence": label["Confidence"]}
                )
            return result

        return {}


# Instance of the ImageModerationProcessor class with the default region
image_processor = ImageModerationProcessor(region_name="us-east-1")
