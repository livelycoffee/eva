from .module import RTTranscriberModule

class RTTranscriberAPI:
    def __init__(self, parent_module):
        self.module: RTTranscriberModule = parent_module

    def start(self) -> None:
        self.module.start()

    def pass_audio(self, audio_chunk) -> None:
        self.module.pass_audio_chunk(audio_chunk=audio_chunk)

    def get_memories(self) -> list:
        memories = self.module.get_stored_memories()
        self.module.clear_stored_memories()
        return memories
