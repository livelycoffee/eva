from eva.core.system.services.api import API

class AppContext:
    def __init__(self):
        self.api: dict = {}

    # def register_service(self, API: API):
    #     def decorator(service: Service):
    #         self.services[API] = service
    #         return service
    #     return decorator
    
    def register_service_api(self, api: API) -> None:
        self.api[api.__class__] = api

    def start(self):
        pass

    def stop(self):
        pass