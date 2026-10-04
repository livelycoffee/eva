from eva.core.system.services.service import Service
from . import stream
import numpy as np

class AudioInputService(Service):
    def __init__(self):
        self.audio_input_stream = stream.AudioInputStream()

    def start(self) -> None:
        self.audio_input_stream.start()

    def stop(self) -> None:
        self.audio_input_stream.stop()
        self.audio_input_stream.shutdown()
    
    def get_audio_chunk(self):
        audio_chunk, _ = self.audio_input_stream.get_chunk()
        # #audio = np.concatenate(audio_chunk, axis=0)
        # audio = audio_chunk.astype(np.float32)
        return audio_chunk
