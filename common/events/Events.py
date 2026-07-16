from __future__ import annotations
from abc import ABC, abstractmethod

class Event(ABC):
    pass

class EventPublisher(ABC):
    def __init__(self):
        self.__observers: list[EventHandler] = []

    def publish(self, event: Event) -> None:
        for observer in self.__observers:
            observer.onChange(event)
        
    def register(self, handler: EventHandler) -> None:
        self.__observers.append(handler)

    def unregister(self, handler: EventHandler) -> None:
        self.__observers = [o for o in self.__observers if o != handler]

class EventHandler(ABC):

    @abstractmethod
    def onChange(event: Event) -> None:
        pass

    def listenTo(self, publisher: EventPublisher):
        publisher.register(self)
