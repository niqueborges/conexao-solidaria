import boto3
import requests
from botocore.exceptions import ClientError
from requests.exceptions import RequestException
from conexao_solidaria.core.config import settings


class Transcribe:
    """
    Class responsible for converting audio to text using Amazon Transcribe.
    """

    def __init__(self) -> None:
        """
        Initializes the TranscribeService by creating a Boto3 client for
        Amazon Transcribe
        """
        self.client = boto3.client("transcribe", region_name=settings.REGION_NAME)

    def transcribe_audio(
        self,
        job_name: str,
        media_uri: str,
        media_format: str,
        language_code: str,
    ) -> dict:
        """
        Transcribe the audio to text.
        """
        try:
            response = self.client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": media_uri},
                MediaFormat=media_format,
                LanguageCode=language_code,
            )
            return response
        except ClientError as e:
            print(f"Erro ocorrido: {e}")
            raise

    def get_transcript(self, job_name: str) -> str:
        """
        Responsible for retrieving the transcription of a job.
        """
        try:
            response = self.client.get_transcription_job(TranscriptionJobName=job_name)
            if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
                transcript_uri = response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]
                return transcript_uri
            else:
                print("A transcrição ainda não foi concluída.")
                return None
        except ClientError as e:
            print(f"Erro ao obter o trabalho de transcrição: {e}")
            raise

    def get_transcript_content(self, transcript_uri: str) -> str:
        """
        Get the text of the completed transcription.
        """
        try:
            transcript_response = requests.get(transcript_uri, timeout=15)
            print(f"Resposta da requests: {transcript_response}")
            transcript_text = transcript_response.json()["results"]["transcripts"][0][
                "transcript"
            ]
            return transcript_text
        except RequestException as e:
            print(f"Erro na requisição HTTP: {e}")
            raise
        except ValueError as e:
            print(f"Erro ao processar o conteúdo JSON: {e}")
            raise
