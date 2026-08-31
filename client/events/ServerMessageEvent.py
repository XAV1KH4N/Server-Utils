from common.events.Events import Event
from messages.common.Serializable import Serializable

class ServerMessageEvent(Event):
    def __init__(self, msg: Serializable):
        self.__msg = msg

    def getMsg(self) -> Serializable:
        return self.__msg
