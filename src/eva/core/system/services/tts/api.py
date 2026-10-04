from eva.core.system.services import API
from .service import TTSService
import numpy as np
from scipy.signal import resample_poly

class TTSAPI(API):
    def __init__(self, parent_service):
        self.service: TTSService = parent_service

    def get_synthesized_audio(self, text: str) -> list:
        audio = self.service.synthesize_from_text(text=text.encode("ascii", "ignore").decode())
        if not audio:
            return np.array([], dtype=np.float32)
        chunks = []
        for chunk in audio:
            data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            chunks.append(data)
        if not chunks:
            return np.array([], dtype=np.float32)
        audio = np.concatenate(chunks)
        audio = audio.astype(np.float32) / 32767.0
        audio_16k = resample_poly(audio, up=320, down=441).astype(np.float32)
        return audio_16k
