from typing import Optional


class BaseCustomException(Exception):
    """Classe base para todas as exceções customizadas."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "Ocorreu um Exceção."
        super().__init__(message or self.message, *args)


class AudioStreamNotFoundException(BaseCustomException):
    """AudioStream não foi encontrado na resposta do Polly."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "AudioStream não foi encontrado na resposta do Polly."
        super().__init__(*args, message=message or self.message)
