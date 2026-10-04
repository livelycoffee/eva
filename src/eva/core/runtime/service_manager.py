from eva.core.system import Service

class ServiceManager:
    def __init__(self):
        self._services: dict = {}

    def register_service(self, service: Service) -> None:
        self._services[service.__class__] = service

    def start_services(self) -> None:
        for service in self._services.values():
            service: Service
            service.start()

    def stop_services(self) -> None:
        for service in self._services.values():
            service: Service
            service.stop()