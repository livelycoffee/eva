from eva.core.system.services.stream import Stream
import sounddevice as sd
from . import BLOCK_SIZE, SAMPLE_RATE
import numpy as np

class AudioInputStream(Stream):
    def __init__(self):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE, 
            channels=1,
            blocksize=BLOCK_SIZE,
            dtype=np.float32
        )

    def start(self) -> None:
        self.stream.start()

    def stop(self) -> None:
        self.stream.stop()

    def shutdown(self) -> None:
        self.stream.close()

    def get_chunk(self) -> tuple:
        return self.stream.read(frames=512)
    
    # def callback(self, indata, frames, time_info, status):
    #     if status:
    #         print(status)
    #     pass
