from typing import Optional


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "An exception occurred."
        super().__init__(message or self.message, *args)


class AudioStreamNotFoundException(BaseCustomException):
    """AudioStream was not found in Polly's response."""

    def __init__(self, *args: object, message: Optional[str] = None) -> None:
        self.message = "AudioStream was not found in Polly's response."
        super().__init__(*args, message=message or self.message)
