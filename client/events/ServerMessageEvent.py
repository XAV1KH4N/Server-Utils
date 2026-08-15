from common.events.Events import Event, EventDesitination, EventOrigin
from messages.common.Serializable import Serializable

class ServerMessageEvent(Event):
    def __init__(self, msg: Serializable):
        self.__msg = msg

    def getMsg(self) -> Serializable:
        return self.__msg

    def get_destination(self):
        return EventDesitination.MESSAGE_HANDLER
    
    def get_origin(self):
        return EventOrigin.COMMUNICATION_HANDLER

