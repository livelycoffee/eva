from eva.core.system.services.service import Service
import torch

class VADService(Service):
    def __init__(self):
        self.model, self.utils = (None, None)

    def start(self) -> None:
        self.model, self.utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad')
        (get_speech_timestamps,
        save_audio,
        read_audio,
        VADIterator,
        collect_chunks) = self.utils

        torch.set_num_threads(1)
    
    def infer(self, audio_chunk) -> float:
        with torch.inference_mode():
            return self.model(torch.from_numpy(audio_chunk), 16000).item()

    def stop(self) -> None:
        if self.model is not None:
            del self.model
