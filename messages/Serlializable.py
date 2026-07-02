from abc import ABC, abstractmethod

class Serializable(ABC):
    ClassName = "className"

    @abstractmethod
    def toMap(self) -> dict:
        """Converts object to a dictionary of primatives"""
        