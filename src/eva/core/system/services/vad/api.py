from eva.core.system.services.api import API

class VADAPI(API):
    def __init__(self, parent_service):
        self.service = parent_service

    def get_confidence(self, audio_chunk) -> float:
        try:
            return self.service.infer(audio_chunk)
        except Exception as e:
            print(f"[VAD]: {e}")
            return 0 
