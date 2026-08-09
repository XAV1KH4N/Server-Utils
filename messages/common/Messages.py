from messages.common.Serializable import Serializable
from common.EncyptUtils import EncryptUtils
import base64

class Message(Serializable):
    MsgProperty = "msg"
    ClassNameProperty = "className"

    def __init__(self, data: Serializable | dict):
        if (isinstance(data, Serializable)):
            self.__msg = data.to_map()
            self.__className = type(data).__name__
        else:
            self.__msg = data[Message.MsgProperty]
            self.__className = data[Message.ClassNameProperty] 

    def to_map(self):
        return {
            Message.MsgProperty: self.__msg,
            Message.ClassNameProperty: self.__className
        }
    
    def get_msg_map(self):
        return self.__msg
    
    def get_class_name(self):
        return self.__className
    
class EncryptedMessageData:
    def __init__(self, cipher: bytes, className: str, iv: bytes):
        self.__cipher = base64.b64encode(cipher).decode(EncryptUtils.ENCODE_TYPE)
        self.__className = className
        self.__iv = base64.b64encode(iv).decode(EncryptUtils.ENCODE_TYPE)

    def getCipher(self) -> str:
        return self.__cipher
    
    def getClassName(self) -> str:
        return self.__className

    def get_iv(self) -> str:
        return self.__iv

class EncryptedMessage(Serializable):
    CipherProperty = "cipher"
    ClassNameProperty = "className"
    IVProperty = "iv"

    def __init__(self, data: EncryptedMessageData | dict):
        if (isinstance(data, EncryptedMessageData)):
            self.__cipher = data.getCipher()
            self.__className = data.getClassName()
            self.__iv = data.get_iv()
        else:
            self.__cipher = data[EncryptedMessage.CipherProperty]
            self.__className = data[EncryptedMessage.ClassNameProperty]
            self.__iv = data[EncryptedMessage.IVProperty]

    def to_map(self):
        return {
            EncryptedMessage.CipherProperty: self.__cipher,
            EncryptedMessage.ClassNameProperty: self.__className,
            EncryptedMessage.IVProperty: self.__iv
        }

    def get_cipher(self) -> str:
        return self.__cipher
    
    def get_cipher_bytes(self) -> bytes:
        return base64.b64decode(self.__cipher)

    def get_iv(self) -> bytes:
        return base64.b64decode(self.__iv)

    def get_class_name(self) -> str:
        return self.__className