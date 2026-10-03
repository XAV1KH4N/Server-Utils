from abc import ABC, abstractmethod
from random import Random

class Serializable(ABC):
    ClassName = "className"

    @abstractmethod
    def to_map(self) -> dict:
        """Converts object to a dictionary of primatives"""
        
class SerializerBuilder(ABC):

    @abstractmethod
    def build_message(self, map: dict) -> Serializable: 
        pass


class Requestable(Serializable):
    RequestIdProperty = "requestId"

    def generate_request_id(self) -> str:
        random = Random()
        return str(random.randint(1, 10000))

    @abstractmethod
    def get_request_id(self) -> str:
        pass

class Responsable(Serializable):

    @abstractmethod
    def get_request_id(self) -> str:
        pass