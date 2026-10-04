from .service import AudioOutputService
from eva.core.system.services.api import API

class AudioOutputAPI(API):
    def __init__(self, parent_service: AudioOutputService):
        self.service = parent_service
    
    def put_audio_chunk(self, chunk) -> None:
        self.service.put_audio_chunk(audio_data=chunk)
