import os
import boto3
import requests
import time
from botocore.exceptions import ClientError
from requests.exceptions import RequestException


class Transcribe:
    """
    Class responsible for converting audio to text using Amazon Transcribe.
    """

    def __init__(self) -> None:
        """
        Initializes the transcription service by creating a Boto3 client for Amazon
        Transcribe.
        """
        self.client = boto3.client("transcribe", region_name=os.getenv("REGION"))

    def transcribe_audio(
        self,
        job_name: str,
        media_uri: str,
        media_format: str,
        language_code: str,
    ) -> dict:
        """
        Starts the audio-to-text transcription.
        """
        try:
            self.client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": media_uri},
                MediaFormat=media_format,
                LanguageCode=language_code,
            )

            while True:
                job_status = self.client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                status = job_status["TranscriptionJob"]["TranscriptionJobStatus"]

                if status == "COMPLETED":
                    print("Transcrição concluída com sucesso.")
                    return job_status
                elif status == "FAILED":
                    print("A transcrição falhou.")
                    raise Exception("O trabalho de transcrição falhou.")

                print("Transcrição em andamento... Aguardando conclusão.")
                time.sleep(10)

        except ClientError as e:
            print(f"Erro ocorrido: {e}")
            raise

    def get_transcript(self, job_name: str) -> str:
        """
        Responsible for retrieving the transcription URI of a completed job.
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
        Retrieves the text from the completed transcription.
        """
        try:
            transcript_response = requests.get(transcript_uri, timeout=30)
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
