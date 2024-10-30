from pydantic import BaseModel, Field


class ScanIn(BaseModel):
    """Input Schema for image scanning."""

    bucket: str = Field(
        description="The S3 bucket where the image is stored.",
        examples=["my-s3-bucket"],
    )
    image_key: str = Field(
        description="The S3 key of the image to be analyzed.",
        examples="images/sample.jpg",
    )
