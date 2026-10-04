import threading
import queue
import numpy as np
from eva.core.runtime import AppContext, EventBus
from eva.core.system.services.speech_transcribe import SpeechTranscribeAPI
from eva.core.system.services.semantic_memory import SemanticMemoryAPI

class RTTranscriberModule(threading.Thread):
    def __init__(self, appctx, event_bus):
        super().__init__(daemon=True)
        self.audio_buffer_q = queue.Queue()
        self.sound_data = []
        self.memories = set()
        
        self.app: AppContext = appctx
        self.event_bus: EventBus = event_bus

    def pass_audio_chunk(self, audio_chunk):
        self.audio_buffer_q.put(audio_chunk)

    def run(self):
        while True:
            try:
                chunk = self.audio_buffer_q.get(timeout=0.3)
            except queue.Empty:
                continue
            self.sound_data.append(chunk)
            audio_data = []

            if len(self.sound_data) >= 35:
                audio_data.extend(self.sound_data[:35].copy())
                self.sound_data = self.sound_data[25:]

                if not audio_data:
                    continue

                audio = np.concatenate(audio_data, axis=0)
                audio = audio.astype(np.float32)
                text = self.app.api[SpeechTranscribeAPI].transcribe_audio(audio.flatten())
                if not text:
                    continue

                memories = self.app.api[SemanticMemoryAPI].get_memories(queries=text)['documents'][0]
                for memory in memories:
                    self.memories.add(memory)

    def clear_stored_memories(self):
        self.memories = set()

    def get_stored_memories(self):
        return list(self.memories)
