from common.events.Events import Event
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage

class KeyExchangeRecievedEvent(Event):
    def __init__(self, key: KeyExchangeInitMessage):
        self.__key = key

    def get_key(self) -> KeyExchangeInitMessage:
        return self.__key