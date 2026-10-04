# ---------- IMPORTS ----------

from .core.runtime.runtime import Runtime
from eva.core.system.services.audio import *
from eva.core.system.services.vad import *
from eva.core.system.services.speech_transcribe import *
from eva.core.system.services.primary_llm import *
from eva.core.system.services.semantic_memory import *
from eva.core.system.services.wakeword import *
from eva.core.system.services.tts import *

# ---------- BOOTSTRAP ----------

def bootstrap():

    runtime = Runtime()
    servm = runtime.service_manager
    app = runtime.app

    _audio_input = AudioInputService()
    servm.register_service(service=_audio_input)
    app.register_service_api(api=AudioInputAPI(parent_service=_audio_input))

    _audio_output = AudioOutputService()
    servm.register_service(service=_audio_output)
    app.register_service_api(api=AudioOutputAPI(parent_service=_audio_output))

    _vad = VADService()
    servm.register_service(service=_vad)
    app.register_service_api(api=VADAPI(parent_service=_vad))

    _speech_transcribe = SpeechTranscribeService()
    servm.register_service(service=_speech_transcribe)
    app.register_service_api(api=SpeechTranscribeAPI(parent_service=_speech_transcribe))

    _primary_llm = PrimaryLLMService()
    servm.register_service(service=_primary_llm)
    app.register_service_api(api=PrimaryLLMAPI(parent_service=_primary_llm))

    _semantic_memory = SemanticMemoryService()
    servm.register_service(service=_semantic_memory)
    app.register_service_api(api=SemanticMemoryAPI(parent_service=_semantic_memory))

    _wake_word = WakeWordService()
    servm.register_service(service=_wake_word)
    app.register_service_api(api=WakeWordAPI(parent_service=_wake_word))

    _tts = TTSService()
    servm.register_service(service=_tts)
    app.register_service_api(api=TTSAPI(parent_service=_tts))

    return runtime

#*---------- END OF CODE ----------*
