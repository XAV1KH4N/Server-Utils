from common.events.ConnectionId import ConnectionID
from common.events.Events import Event, EventWithId, EventDesitination, EventOrigin
from messages.common.Messages import EncryptedMessage

class EncryptedMessageEvent(EventWithId):
    def __init__(self, msg: EncryptedMessage, id: ConnectionID):
        self.__msg = msg
        self.__id = id

    def get_id(self) -> ConnectionID:
        return self.__id

    def get_msg(self) -> EncryptedMessage:
        return self.__msg
    
    def get_destination(self) -> EventDesitination:
        return EventDesitination.SERVER

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER

        