from messages.common.Serlializable import Serializable
from messages.common.Messages import Message, EncryptedMessage, EncryptedMessageData
from common.EncyptUtils import EncryptUtils
import json

class MessageBuilder:
    def __init__(self):
        pass

    def build_message_bytes(self, msg: Serializable) -> bytes: 
        final_msg = Message(msg)
        json_data = json.dumps(final_msg.to_map()).encode(EncryptUtils.ENCODE_TYPE)
        return json_data

    def rebuild_message(self, data: bytes) -> Serializable:
        decoded = data.decode(EncryptUtils.ENCODE_TYPE)
        received_data: dict = json.loads(decoded)
        msg = Message(received_data)
        map = msg.getMsgMap()
        class_name = msg.getClassName()
        match class_name:
            case "EncryptedMessage": 
                return EncryptedMessage(map) 
            case _:
                raise Exception("Message class not found")  


# Take message (Probably encrypted, throw error if not)
# Turn to json and back