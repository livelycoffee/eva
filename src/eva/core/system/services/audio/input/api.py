from .service import AudioInputService
from eva.core.system.services.api import API
import numpy as np

class AudioInputAPI(API):
    '''
    ### APIs:
        get_frame()
    '''
    def __init__(self, parent_service: AudioInputService):
        self.service = parent_service
    
    def get_audio_chunk(self) -> np.typing.NDArray[np.float32]:
        return self.service.get_audio_chunk()
