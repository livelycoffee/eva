from eva.core.system.services import Service

import openwakeword
from openwakeword.model import Model
import threading
import numpy as np
from pathlib import Path

file_path = Path(__file__)
src_path = file_path.parents[6]
model_path = str(src_path / "models/wakeword/default.onnx")

class _WakewordModelFlushCoworker(threading.Thread):
    def __init__(self, model, lock):
        super().__init__(daemon=True)
        self.model: Model = model
        self.model_lock: threading.Lock = lock

    def run(self):
        with self.model_lock:
            _pr = self.model.predict(np.zeros(32000).astype(np.int16))


class WakeWordService(Service):
    def __init__(self):
        self.model: Model = None
        self.lock = threading.Lock()

    def start(self):
        openwakeword.utils.download_models()
        self.model = Model(
            wakeword_models=[model_path],
            inference_framework="onnx"
        )
    
    def stop(self):
        if self.model is not None:
            with self.lock:
                del self.model

    def get_prediction(self, audio_chunk):
        with self.lock:
            prediction = self.model.predict(audio_chunk).get("default", 0.0)
        return prediction

    def force_flush_model(self) -> None:
        with self.lock:
            self.model.prediction_buffer.clear()
        _wwmf_coworker = _WakewordModelFlushCoworker(model=self.model, lock=self.lock)
        _wwmf_coworker.start()
