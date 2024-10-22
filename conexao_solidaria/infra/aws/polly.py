import boto3
from conexao_solidaria.core.config import settings
from conexao_solidaria.core.exceptions import AudioStreamNotFoundException


class Polly:
    def __init__(self) -> None:
        self.client = boto3.client("polly", region_name=settings.REGION_NAME)

    def convert(self, text: str, file_name: str) -> tuple[bytes, str]:
        """Converts text to MP3 audio. Returns the content and file name."""

        response = self.client.synthesize_speech(
            Engine="neural", Text=text, OutputFormat="mp3", VoiceId="Camila"
        )

        # Raises an exception if AudioStream is not in the response
        if "AudioStream" not in response:
            raise AudioStreamNotFoundException()

        return response["AudioStream"].read(), f"{file_name}.mp3"
