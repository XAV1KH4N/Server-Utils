import os
from messages.common.Serlializable import Serializable, SerializerBuilder
from messages.common.Messages import EncryptedMessage, EncryptedMessageData
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from common.EncyptUtils import EncryptUtils
import json 

class EncryptMessageBuilder:
    def __init__(self, k: int, builder: SerializerBuilder):
        self.iv = os.urandom(EncryptUtils.BLOCK_SIZE)
        self.key = k.to_bytes(EncryptUtils.KEY_SIZE, byteorder='big')
        self.backend = default_backend()
        self.__cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        self.__message_builder = builder

    def build_message(self, msg: Serializable) -> EncryptedMessage:
        msg_map = msg.to_map()
        json_data = json.dumps(msg_map).encode(EncryptUtils.ENCODE_TYPE)
        json_enctyped = self.__encrypt(json_data)
        class_name = type(msg).__name__
        data = EncryptedMessageData(json_enctyped, class_name)
        enc_msg = EncryptedMessage(data)
        return enc_msg
    
    def __encrypt(self, data: bytes) -> bytes:
        padder = padding.ANSIX923(128).padder() 
        pad_data = padder.update(data) + padder.finalize()

        encryptor = self.__cipher.encryptor()
        ct = encryptor.update(pad_data) + encryptor.finalize()
        return ct
    
    def __decrypt(self, cipher: bytes) -> bytes:
        unpadder = padding.ANSIX923(128).unpadder() 
        decryptor = self.__cipher.decryptor()
        pad_data = decryptor.update(cipher) + decryptor.finalize()
        raw = unpadder.update(pad_data) + unpadder.finalize()
        return raw
    
    def recreate_message(self, msg: EncryptedMessage) -> Serializable:
        text = self.__decrypt(msg.getCipherBytes())
        map: dict = json.loads(text.decode(EncryptUtils.ENCODE_TYPE))
        class_name = msg.getClassName()
        return self.__message_builder.build_message(map, class_name)
