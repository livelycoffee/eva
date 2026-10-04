from eva.core.system.services import API
from .service import SpeechTranscribeService

class SpeechTranscribeAPI(API):
    def __init__(self, parent_service):
        self.service: SpeechTranscribeService = parent_service

    def transcribe_audio(self, audio):
        return self.service.transcribe(audio)
