from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import Message
from messages.common.Serializable import Serializable
from messages.common.TextMessage import TextMessage
from teminal.common.messages.Broadcast import BroadcastMessage

class CMDMessageBuilder(MessageBuilder):
    def extract_message(self, message: Message) -> Serializable:
        print("CMD message builder", message.get_class_name())
        msg = super().extract_message(message)
        if (msg != None):
            print("Returned early, found message")
            return msg

        msg_map = message.get_msg_map()
        print("(CMD)", message.get_class_name() == BroadcastMessage.__name__)
        match message.get_class_name():
            case BroadcastMessage.__name__:
                print("cmd - bcm")
                return BroadcastMessage(msg_map)
            case _:
                print("Unexpected message wrapped (CMD)") 
                return None