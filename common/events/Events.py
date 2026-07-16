from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

class Event(ABC):
    
    @abstractmethod
    def getDestination(self) -> EventDesitination:
        pass 

    @abstractmethod
    def getOrigin(self) -> EventOrigin:
        pass 

class EventDesitination(Enum):
    ALL = 0
    MESSAGE_HANDLER = 1
    COMMUNICATION_HANDLER = 2
    SERVER = 3
    CLIENT = 4

class EventOrigin(Enum):
    MESSAGE_HANDLER = 1
    COMMUNICATION_HANDLER = 2
    SERVER = 3
    CLIENT = 4

class EventPublisher(ABC):
    def __init__(self):
        self.__observers: list[EventHandler] = []

    def publish(self, event: Event) -> None:
        for observer in self.__observers:
            observer.on_change(event)
        
    def register(self, handler: EventHandler) -> None:
        self.__observers.append(handler)

    def unregister(self, handler: EventHandler) -> None:
        self.__observers = [o for o in self.__observers if o != handler]

class EventHandler(ABC):

    @abstractmethod
    def on_change(self, event: Event) -> None:
        pass

    def listenTo(self, publisher: EventPublisher):
        publisher.register(self)
