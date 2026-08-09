import os
from messages.common.Serializable import Serializable, SerializerBuilder
from messages.common.Messages import EncryptedMessage, EncryptedMessageData, Message
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from common.EncyptUtils import EncryptUtils
import json 

class EncryptMessageBuilder:
    def __init__(self, k: int, builder: SerializerBuilder):
        self.iv = os.urandom(EncryptUtils.BLOCK_SIZE) # Does IV need to be the same for the client and server? YES. Reconstruct each time with the message
        self.key = k.to_bytes(EncryptUtils.KEY_SIZE, byteorder='big')
        self.backend = default_backend()
        self.__message_builder = builder

    def build_message(self, msg: Serializable) -> EncryptedMessage:
        msg_map = msg.to_map()
        json_data = json.dumps(msg_map).encode(EncryptUtils.ENCODE_TYPE)
        json_enctyped = self.__encrypt(json_data)
        class_name = type(msg).__name__
        data = EncryptedMessageData(json_enctyped, class_name, self.iv)
        enc_msg = EncryptedMessage(data)
        return enc_msg
    
    def __encrypt(self, data: bytes) -> bytes:
        print("Encrypting", data)
        padder = padding.ANSIX923(128).padder() 
        pad_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ct = encryptor.update(pad_data) + encryptor.finalize()

        return ct
    
    def __decrypt(self, cipher: bytes, iv: bytes) -> bytes:
        print("Decrypting", cipher)
        unpadder = padding.ANSIX923(128).unpadder() 
        c = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = c.decryptor()
        pad_data = decryptor.update(cipher) + decryptor.finalize()
        raw = unpadder.update(pad_data) + unpadder.finalize()
        print("Decrypted", raw)
        return raw
    
    def recreate_message(self, msg: EncryptedMessage) -> Serializable:
        iv = msg.get_iv()
        text = self.__decrypt(msg.get_cipher_bytes(), iv)
        class_name = msg.get_class_name()
        print("Decrypted Bytes", text)
        map: dict = json.loads(text.decode(EncryptUtils.ENCODE_TYPE))
        built_msg = {
            Message.ClassNameProperty: class_name,
            Message.MsgProperty: map
        }
        return self.__message_builder.build_message(built_msg)
