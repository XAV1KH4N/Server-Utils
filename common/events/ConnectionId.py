from __future__ import annotations
from random import Random

class ConnectionID:
    def __init__(self, addr):
        self.__addr = addr
        self.__id = (Random().randint(0, 100000))

    def is_id(self, id: ConnectionID) ->  bool:
        return id.get_id() == self.__id

    def get_id(self) -> int:
        return self.__id