from messages.common.TextMessage import TextMessage
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage, KeyExchangeResponseMessage
from messages.common.Serializable import Serializable, SerializerBuilder
from messages.common.Messages import Message, EncryptedMessage
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder
from common.EncyptUtils import EncryptUtils
import json

class MessageBuilder(SerializerBuilder):

    def build_message(self, map: dict) -> Serializable: 
        return self.extract_message(Message(map))

    def build_encrypted_message_bytes(self, msg: Serializable, enc_builder: EncryptMessageBuilder) -> bytes:
        enc_msg = enc_builder.build_message(msg)
        final_msg = Message(enc_msg)
        json_data = json.dumps(final_msg.to_map()).encode(EncryptUtils.ENCODE_TYPE)
        return json_data

    def build_message_bytes(self, msg: Serializable) -> bytes: 
        final_msg = Message(msg)
        json_data = json.dumps(final_msg.to_map()).encode(EncryptUtils.ENCODE_TYPE)
        return json_data
    
    def extract_message(self, message: Message) -> Serializable:        
        msg_map = message.get_msg_map()
        match message.get_class_name():
            case KeyExchangeInitMessage.__name__:
                return KeyExchangeInitMessage(msg_map)
            case KeyExchangeResponseMessage.__name__:
                return KeyExchangeResponseMessage(msg_map)
            case EncryptedMessage.__name__:
                return EncryptedMessage(msg_map)
            case TextMessage.__name__:
                return TextMessage(msg_map)
            case _:
                print("Unexpected message wrapped") 

    def rebuild_message(self, data: bytes) -> Message:
        decoded = data.decode(EncryptUtils.ENCODE_TYPE)
        received_data: dict = json.loads(decoded)
        msg = Message(received_data)
        return self.extract_message(msg)