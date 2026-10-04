from eva.core.runtime import AppContext, EventBus

from eva.core.system.services.audio import AudioInputAPI, AudioOutputAPI
from eva.core.system.services.vad import VADAPI
from eva.core.system.services.speech_transcribe import SpeechTranscribeAPI
from eva.core.system.services.primary_llm import PrimaryLLMAPI
from eva.core.system.services.wakeword import WakeWordAPI
from eva.core.system.services.tts import TTSAPI

from eva.modules._rt_transcriber import RTTranscriberModule, RTTranscriberAPI

from collections import deque
import time
import numpy as np

AUDIO_BUFFER_DQ_LENGTH = 10

class ConversationalLoop:
    def __init__(self, appctx: AppContext, eventbus: EventBus):
        self.app = appctx
        self.bus = eventbus

        self.audio_buffer_dq = deque(maxlen=AUDIO_BUFFER_DQ_LENGTH)
        self.listening = False
        self.speaking = False
        self.sound_data = []

        self.prev_time = time.time()
        self.rtt_module = RTTranscriberModule(appctx=self.app, event_bus=self.bus)

    def start(self):
        # Caching Service APIs
        self.audio_input: AudioInputAPI = self.app.api[AudioInputAPI]
        self.audio_output: AudioOutputAPI = self.app.api[AudioOutputAPI]
        self.wakeword: WakeWordAPI = self.app.api[WakeWordAPI]
        self.vad: VADAPI = self.app.api[VADAPI]
        self.primary_llm: PrimaryLLMAPI = self.app.api[PrimaryLLMAPI]
        self.speech_transcribe: SpeechTranscribeAPI = self.app.api[SpeechTranscribeAPI]
        self.tts: TTSAPI = self.app.api[TTSAPI]

        # Caching Module APIs
        self.rtt = RTTranscriberAPI(parent_module=self.rtt_module)

        self.rtt.start()

    def wakeword_check(self):
        print("\nWaiting for wakeword...")

        while True:
            chunk = self.audio_input.get_audio_chunk()
            chunk = (chunk*32767).astype(np.int16)
            prediction = self.wakeword.get_confidence(audio_chunk=chunk.flatten())

            if prediction >= 0.9:
                print("Recognised.")
                self.wakeword.flush_model()
                break

    def run(self):
        self.listening = True
        self.prev_time = time.time()
        self.speaking = False
        self.audio_buffer_dq.clear()

        print("\nListening...")
        while True:
            chunk = self.audio_input.get_audio_chunk()
            self.audio_buffer_dq.append(chunk)
            self.rtt.pass_audio(audio_chunk=chunk)

            speech_confidence = self.vad.get_confidence(chunk.flatten())

            if speech_confidence >= 0.7 and self.listening:
                if not self.speaking:
                    self.sound_data.extend(list(self.audio_buffer_dq)[:-1])
                    self.speaking = True
                self.prev_time = time.time()

            if self.speaking and self.listening:
                self.sound_data.append(chunk)

            if ((time.time() - self.prev_time) >= 1.7) and self.speaking and self.listening:
                break
            
        time.sleep(0.1) # --> Smoother transition to end of audio stream input
        sound_data = self.sound_data
        self.sound_data = []
        self.audio_buffer_dq.clear()

        self.listening = False
        self.speaking = False

        audio = np.concatenate(sound_data, axis=0)
        audio = audio.astype(np.float32)
        duration = len(audio)/16000
        print(f"Recorded. ({duration}s)")

        memories = self.rtt.get_memories()
        memories_final = ", ".join(memory for memory in memories)

        text = self.speech_transcribe.transcribe_audio(audio.flatten())
        print(f"\nUSER: {text}")
        
        response = self.primary_llm.get_llm_response(query=text, memories=memories_final)
        print(f"\nEVA: {response}")
        response_speech = self.tts.get_synthesized_audio(text=response)
        for chunk in response_speech:
            self.audio_output.put_audio_chunk(chunk=chunk)
