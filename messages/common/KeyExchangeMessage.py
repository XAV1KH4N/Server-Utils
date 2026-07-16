import base64
from messages.common.Serializable import Serializable

class KeyExchangeData:
    def __init__(self, Y: int, signature: bytes, base: int, prime: int):
        self.__Y: int = Y
        self.__signature: bytes = signature
        self.__base: int = base
        self.__prime: int = prime

    def getY(self) -> int:
        return self.__Y

    def getSignature(self) -> bytes:
        return self.__signature
    
    def getBase(self) -> int:
        return self.__base

    def getPrime(self) -> int:
        return self.__prime
        
class KeyExchangeInitMessage(Serializable):
    YProperty = "Y"
    SignatureProperty = "signature"
    BaseProperty = "base"
    PrimeProperty = "prime"

    def __init__(self, data: KeyExchangeData | dict):
        if (isinstance(data, KeyExchangeData)):
            self.__Y: int = data.getY()
            self.__signature: bytes = data.getSignature()
            self.__base: int = data.getBase()
            self.__prime: int = data.getPrime()
        else:
            data_str = data[KeyExchangeInitMessage.SignatureProperty]
            data_bytes = self.__encode(data_str)
            self.__Y: int = data[KeyExchangeInitMessage.YProperty]
            self.__signature: bytes = data_bytes
            self.__base: int = data[KeyExchangeInitMessage.BaseProperty]
            self.__prime: int = data[KeyExchangeInitMessage.PrimeProperty]

    def to_map(self) -> dict:
        return {
          KeyExchangeInitMessage.YProperty: self.__Y,
          KeyExchangeInitMessage.BaseProperty: self.__base,
          KeyExchangeInitMessage.PrimeProperty: self.__prime,
          KeyExchangeInitMessage.SignatureProperty: self.__decode(self.__signature)
        } 
    
    def getY(self) -> int:
        return self.__Y

    def getSignature(self) -> bytes:
        return self.__signature
    
    def getBase(self) -> int:
        return self.__base

    def getPrime(self) -> int:
        return self.__prime

    def __encode(self, string: str) -> bytes:
        return base64.b64decode(string)
    
    def __decode(self, data: bytes) -> str: 
        return base64.b64encode(self.__signature).decode('utf-8')
    