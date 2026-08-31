from __future__ import annotations
from abc import ABC, abstractmethod

from common.events.ConnectionId import ConnectionID

class Event(ABC):
    pass # All events should include id
    
class EventWithId(Event):
    
    @abstractmethod
    def get_id(self) -> ConnectionID:
        pass 
        
class EventHandler(ABC):

    @abstractmethod
    def on_change(self, event: Event) -> None:
        pass
