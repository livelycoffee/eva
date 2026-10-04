from eva.core.system.services.stream import Stream
import sounddevice as sd
import numpy as np
from numpy.typing import NDArray
from . import BLOCK_SIZE, SAMPLE_RATE

class AudioOutputStream(Stream):
    def __init__(self):
        self.stream = sd.OutputStream(
            samplerate=16000, 
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

    def put_frame(self, data: NDArray) -> None:
        return self.stream.write(data=data)
