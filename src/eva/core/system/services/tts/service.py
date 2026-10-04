from eva.core.system.services import Service
from piper.voice import PiperVoice
from typing import Iterable
from piper import AudioChunk
from pathlib import Path

file_path = Path(__file__)
src_path = file_path.parents[6]
model_path = str(src_path / "models/tts/piper/en_US-hfc_female-medium.onnx")

class TTSService(Service):
    def __init__(self):
        self.voice = None
        self.sample_rate = 16000

    def start(self) -> None:
        self.voice = PiperVoice.load(model_path=model_path)
    
    def stop(self) -> None:
        if self.voice is not None:
            del self.voice

    def synthesize_from_text(self, text: str) -> Iterable[AudioChunk]:
        return self.voice.synthesize(text)
