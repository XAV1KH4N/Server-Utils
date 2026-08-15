from common.events.Events import Event, EventDesitination, EventOrigin
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage

class KeyExchangeRecievedEvent(Event):
    def __init__(self, key: KeyExchangeInitMessage):
        self.__key = key

    def get_key(self) -> KeyExchangeInitMessage:
        return self.__key
    
    def get_destination(self) -> EventDesitination:
        return EventDesitination.KEY_EXCHANGE_HANDLER

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER
