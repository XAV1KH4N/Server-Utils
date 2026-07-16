from abc import ABC, abstractmethod

class Serializable(ABC):
    #ClassName = "className"

    @abstractmethod
    def to_map(self) -> dict:
        """Converts object to a dictionary of primatives"""
        
class SerializerBuilder(ABC):

    @abstractmethod
    def build_message(self, map: dict) -> Serializable: 
        pass

