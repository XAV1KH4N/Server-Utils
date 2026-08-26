from Server.handler.MessageHandler import MessageHandler
from common.events.ConnectionId import ConnectionID
from common.events.Events import Event, EventDesitination, EventOrigin, EventWithId
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import Message
from messages.common.Serializable import Serializable
from teminal.common.messages.Broadcast import BroadcastMessage
from teminal.server.CMDMessageBuilder import CMDMessageBuilder

class CMDMessageHandler(MessageHandler):
    def _create_message_builder(self) -> MessageBuilder:
        return CMDMessageBuilder()

    def extract_message(self, message: Message) -> Serializable:        
        print("Extract messge (CMD)")
        msg = super().extract_message(message)

        if (msg != None):
            print("Returned early, found message (CMD)")
            return msg

        msg_map = message.get_msg_map()
        
        match message.get_class_name():
            case BroadcastMessage.__name__:
                return BroadcastMessage(msg_map)
            case _:
                print("Unexpected message wrapped (CMD)") 
                return None

    def handle_msg(self, msg: Serializable, id: ConnectionID):
        handled = super().handle_msg(msg, id)

        if (handled):
            return True

        match msg:
            case BroadcastMessage():
                self.publish(BroadcastAllEvent(msg.getText(), id))
            case _ :
                print("Unhandled client message (CMD)", msg.__class__.__name__) 
                return False
        return True


class BroadcastAllEvent(EventWithId):
    def __init__(self, text: str, id: ConnectionID):
        self.id: ConnectionID = id
        self.text: str = text

    def get_text(self) -> str:
        return self.text

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER

    def get_destination(self) -> EventDesitination:
        return EventDesitination.COMMUNICATION_HANDLER 

    def get_id(self) -> ConnectionID:
        return self.id        

