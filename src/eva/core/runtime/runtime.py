from eva.core.runtime import AppContext, ServiceManager, EventBus, StreamBus
import eva.behaviour as bh
import time

class Runtime:
    def __init__(self):
        self.app = AppContext()
        self.service_manager = ServiceManager()
        self.event_bus = EventBus()
        self.stream_bus = StreamBus()

    def start(self) -> None:
        self.app.start()
        self.service_manager.start_services()
        print("\nServices started...")

        conv_loop = bh.ConversationalLoop(appctx = self.app, eventbus=self.event_bus)
        conv_loop.start()
        while True:
            try:
                # conv_loop.wakeword_check() --> Future Capability (WIP)
                conv_loop.run()
            except KeyboardInterrupt:
                break

        print("\nWaiting for interrupt...")
        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                break

    def stop(self) -> None:
        self.app.stop()
        self.service_manager.stop_services()
        print("\nServices stopped...")
