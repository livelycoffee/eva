from eva.core.system.services import Service
from faster_whisper import WhisperModel

class SpeechTranscribeService(Service):
    def __init__(self):
        self.model = None

    def start(self):
        self.model = WhisperModel("small.en", device="cpu", compute_type="int8")
    
    def stop(self):
        if self.model is not None:
            del self.model

    def transcribe(self, audio):
        try:
            segments, info = self.model.transcribe(audio, language = "en", task="transcribe", condition_on_previous_text=False, vad_filter=True)
            # print(info)
            query = "".join([segment.text.strip() for segment in segments])
            return query
        except Exception as e:
            print(f"[ERR - FS_Transcriber]: {e}")
            return ""