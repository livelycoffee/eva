from eva.core.system.services.service import Service
from . import stream
import numpy as np

class AudioOutputService(Service):
    def __init__(self):
        self.audio_output_stream = stream.AudioOutputStream()

    def start(self) -> None:
        self.audio_output_stream.start()

    def stop(self) -> None:
        self.audio_output_stream.stop()
        self.audio_output_stream.shutdown()
    
    def put_audio_chunk(self, audio_data: np.typing.NDArray[np.float32]) -> None:
        self.audio_output_stream.put_frame(audio_data)
