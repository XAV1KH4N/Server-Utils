from common.logging.Logger import Logger
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import Message
from messages.common.Serializable import Serializable
from terminal.common.messages.Broadcast import BroadcastMessage

class CMDMessageBuilder(MessageBuilder, Logger):
    def extract_message(self, message: Message) -> Serializable:
        self.logInfo("CMD message builder", message.get_class_name())
        msg = super().extract_message(message)
        if (msg != None):
            self.logInfo("Returned early, found message")
            return msg

        msg_map = message.get_msg_map()
        self.logInfo("(CMD)", message.get_class_name() == BroadcastMessage.__name__)
        match message.get_class_name():
            case BroadcastMessage.__name__:
                self.logDebug("cmd - bcm")
                return BroadcastMessage(msg_map)
            case _:
                self.logError("Unexpected message wrapped (CMD)") 
                return None