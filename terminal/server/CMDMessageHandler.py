from Server.handler.MessageHandler import MessageHandler
from common.events.ConnectionId import ConnectionID
from common.events.Events import EventWithId
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import Message
from messages.common.Serializable import Serializable
from terminal.common.messages.Broadcast import BroadcastMessage
from terminal.server.CMDMessageBuilder import CMDMessageBuilder

class CMDMessageHandler(MessageHandler):
    def _create_message_builder(self) -> MessageBuilder:
        return CMDMessageBuilder()

    def handle_msg(self, msg: Serializable, id: ConnectionID):
        handled = super().handle_msg(msg, id)

        if (handled):
            return True

        match msg:
            case BroadcastMessage():
                self.event_bus.publish(BroadcastAllEvent(msg.getText(), id))
            case _ :
                self.logError("Unhandled client message (CMD)", msg.__class__.__name__) 
                return False
        return True


class BroadcastAllEvent(EventWithId):
    def __init__(self, text: str, id: ConnectionID):
        self.id: ConnectionID = id
        self.text: str = text

    def get_text(self) -> str:
        return self.text

    def get_id(self) -> ConnectionID:
        return self.id        

