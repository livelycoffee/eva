from eva.core.system.services import API
from .service import WakeWordService

class WakeWordAPI:
    def __init__(self, parent_service):
        self.service: WakeWordService = parent_service

    def get_confidence(self, audio_chunk) -> float:
        return self.service.get_prediction(audio_chunk=audio_chunk)

    def flush_model(self) -> None:
        self.service.force_flush_model()
