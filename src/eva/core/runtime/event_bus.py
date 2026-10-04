from eva.core.system.services.event import Event
from collections.abc import Callable
from typing import Any

Handler = Callable[[Event], None]

class EventBus:
    def __init__(self):
        self.events: dict[type[Event], list[Handler]] = {}

    def subscribe(self, event: type[Event]) -> Any:
        def decorator(func):
            self.events.setdefault(event, []).append(func)
            return func
        return decorator
    
    def publish(self, event: Event) -> None:
        for func in self.events.get(type(event), []):
            func(event)
