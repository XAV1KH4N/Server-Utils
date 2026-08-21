from random import Random

class ConnectionID:
    def __init__(self, addr):
        self.__addr = addr
        self.__id = (Random().randint(0, 100000))

    def is_id(self, id: int) ->  bool:
        return id == self.__id