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
    
    def getMsgMap(self):
        return self.__msg
    
    def getClassName(self):
        return self.__className
    
class EncryptedMessageData:
    def __init__(self, cipher: bytes, className: str):
        self.__cipher = base64.b64encode(cipher).decode(EncryptUtils.ENCODE_TYPE)
        self.__className = className

    def getCipher(self) -> str:
        return self.__cipher
    
    def getClassName(self) -> str:
        return self.__className

class EncryptedMessage(Serializable):
    CipherProperty = "cipher"
    ClassNameProperty = "className"

    def __init__(self, data: EncryptedMessageData | dict):
        if (isinstance(data, EncryptedMessageData)):
            self.__cipher = data.getCipher()
            self.__className = data.getClassName()
        else:
            self.__cipher = data[EncryptedMessage.CipherProperty]
            self.__className = data[EncryptedMessage.ClassNameProperty]

    def to_map(self):
        return {
            EncryptedMessage.CipherProperty: self.__cipher,
            EncryptedMessage.ClassNameProperty: self.__className
        }

    def getCipher(self) -> str:
        return self.__cipher
    
    def getCipherBytes(self) -> bytes:
        return base64.b64decode(self.__cipher)

    def getClassName(self) -> str:
        return self.__className