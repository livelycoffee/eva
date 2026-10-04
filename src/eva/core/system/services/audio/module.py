# from eva.core.runtime import Runtime
# from . import AudioInputAPI, AudioInputService
# from . import AudioOutputAPI, AudioOutputService

# class Audio:
#     def __init__(self, runtime: Runtime):
#         self.runtime = runtime
#         self.service = {
#             AudioInputService: AudioInputService(),
#             AudioOutputService: AudioOutputService()
#         }
#         self.api = {
#             AudioInputAPI: AudioInputAPI(self.service[AudioInputService]), 
#             AudioOutputAPI: AudioOutputAPI(self.service[AudioOutputService])
#         }

#     def initialise(self):
#         for api in self.api:
#             self.runtime.app.register_service_api(api=self.api[api], api_class=api)