import os
import requests
from typing import Optional, Tuple
from domain.interfaces import (
    InstitutionRepository,
    AddressProvider,
    ImageModerationService,
    SpeechService,
    ConversationEngine,
)
from infrastructure.api import ApiClient
from infrastructure.via_cep_api import ViaCepService
from infrastructure.polly import generate_audio_as_bytes
from infrastructure.s3 import upload_file_to_s3
from infrastructure.aws import AmazonServices
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

class ApiGatewayInstitutionRepository(InstitutionRepository):
    def __init__(self):
        self.api_client = ApiClient(os.getenv("BASE_URL"))
        self.amazon_services = AmazonServices(self.api_client)

    @tracer.capture_method
    def create(self, institution_data: dict) -> None:
        self.amazon_services.create_institution(institution_data)

class ViaCepProvider(AddressProvider):
    def __init__(self):
        self.api_client = ApiClient(os.getenv("BASE_VIA_CEP"))
        self.via_cep = ViaCepService(self.api_client)

    @tracer.capture_method
    def get_address(self, cep: str) -> Optional[Tuple[str, str, str, str, str]]:
        address_data = self.via_cep.get_cep(cep)
        if address_data:
            return self.via_cep.format_cep_response(address_data)
        return None

class RekognitionModerationService(ImageModerationService):
    def __init__(self):
        self.rekognition_endpoint = os.getenv("REKOGNITION_ENDPOINT")
        self.bucket_name = os.getenv("BUCKET_NAME")

    @tracer.capture_method
    def is_safe(self, image_path: str) -> bool:
        rek_resp = requests.post(
            self.rekognition_endpoint,
            json={"bucket": self.bucket_name, "image_key": image_path},
        )
        return rek_resp.status_code == 204

class PollySpeechService(SpeechService):
    def __init__(self):
        self.bucket_name = os.getenv("BUCKET_NAME")

    @tracer.capture_method
    def generate_audio_url(self, text: str) -> str:
        audio_bytes = generate_audio_as_bytes(text)
        media_key = upload_file_to_s3(audio_bytes, "audio")
        return f"https://{self.bucket_name}.s3.amazonaws.com/{media_key}"


