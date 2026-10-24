from abc import ABC, abstractmethod

from messages.common.Serializable import Requestable

class RequestWorker(ABC):

    @abstractmethod
    def get_request() -> Requestable:
        pass

    @abstractmethod
    def response_event_type(): # Each response message will get turned to an event via the message handler
        pass

    @abstractmethod
    def on_complete(self, result) -> None:
        pass

    @abstractmethod
    def on_failure(self) -> None:
        pass

