from typing import Protocol, Optional, Dict, Tuple

class InstitutionRepository(Protocol):
    def create(self, institution_data: dict) -> None:
        ...

class AddressProvider(Protocol):
    def get_address(self, cep: str) -> Optional[Tuple[str, str, str, str, str]]:
        """Returns: (street, neighborhood, city, state, region) or None if invalid."""
        ...

class ImageModerationService(Protocol):
    def is_safe(self, image_path: str) -> bool:
        ...

class SpeechService(Protocol):
    def generate_audio_url(self, text: str) -> str:
        ...

class ConversationEngine(Protocol):
    def process(self, prompt: str) -> str:
        ...
