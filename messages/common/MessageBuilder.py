from messages.common.KeyExchangeMessage import KeyExchangeInitMessage
from messages.common.Serializable import Serializable
from messages.common.Messages import Message
from common.EncyptUtils import EncryptUtils
import json

class MessageBuilder:
    def __init__(self):
        pass

    def build_message_bytes(self, msg: Serializable) -> bytes: 
        final_msg = Message(msg)
        json_data = json.dumps(final_msg.to_map()).encode(EncryptUtils.ENCODE_TYPE)
        return json_data
    
    def extract_message(self, message: Message) -> Serializable:        
        match message.get_class_name():
            case KeyExchangeInitMessage.__name__:
                return KeyExchangeInitMessage(message.get_msg_map())
            case _:
                print("Unexpected message wrapped") 

    def rebuild_message(self, data: bytes) -> Message:
        decoded = data.decode(EncryptUtils.ENCODE_TYPE)
        received_data: dict = json.loads(decoded)
        msg = Message(received_data)
        return msg