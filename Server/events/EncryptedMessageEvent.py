from common.events.Events import Event, EventDesitination, EventOrigin
from messages.common.Messages import EncryptedMessage

class EncryptedMessageEvent(Event):
    def __init__(self, msg: EncryptedMessage):
        self.__msg = msg

    def get_msg(self) -> EncryptedMessage:
        return self.__msg
    
    def get_destination(self) -> EventDesitination:
        return EventDesitination.SERVER

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER

        