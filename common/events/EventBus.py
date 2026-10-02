from common.events.Events import Event, EventHandler, EventWithId
from common.logging.Logger import Logger

class EventBus(Logger):
    __INSTANCES = 0

    def __init__(self):
        EventBus.__INSTANCES += 1
        self.__handlers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self.__handlers.append(handler)

    def unsubscribe(self, handler: EventHandler) -> None:
        self.__handlers.remove(handler)

    def publish(self, event: Event) -> None:
        self.logInfo("Publish:", event.__class__.__name__)
        for handler in self.__handlers:
            handler.on_change(event)

    def dispose(self) -> None:
        EventBus.__INSTANCES += -1

    def is_valid(self) -> bool:
        return EventBus.__INSTANCES == 1 

    def count(self) -> int:
        return len(self.__handlers)