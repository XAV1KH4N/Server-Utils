import base64
from messages.common.Serializable import Serializable

class KeyExchangeData:
    def __init__(self, Y: int, signature: bytes, base: int, prime: int):
        self.__Y: int = Y
        self.__signature: bytes = signature
        self.__base: int = base
        self.__prime: int = prime

    def get_Y(self) -> int:
        return self.__Y

    def get_signature(self) -> bytes:
        return self.__signature
    
    def get_base(self) -> int:
        return self.__base

    def get_prime(self) -> int:
        return self.__prime
        
class KeyExchangeResponseMessage(Serializable):
    YProperty = "Y"

    def __init__(self, data: int | dict):
        if (isinstance(data, int)):
            self.__Y: int = data
        else:
            self.__Y: int = data[KeyExchangeInitMessage.YProperty]

    def to_map(self) -> dict:
        return {
          KeyExchangeInitMessage.YProperty: self.__Y,
        } 
    
    def get_Y(self) -> int:
        return self.__Y

class KeyExchangeInitMessage(Serializable):
    YProperty = "Y"
    SignatureProperty = "signature"
    BaseProperty = "base"
    PrimeProperty = "prime"

    def __init__(self, data: KeyExchangeData | dict):
        if (isinstance(data, KeyExchangeData)):
            self.__Y: int = data.get_Y()
            self.__signature: bytes = data.get_signature()
            self.__base: int = data.get_base()
            self.__prime: int = data.get_prime()
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
    
    def get_Y(self) -> int:
        return self.__Y

    def get_signature(self) -> bytes:
        return self.__signature
    
    def get_base(self) -> int:
        return self.__base

    def get_prime(self) -> int:
        return self.__prime

    def __encode(self, string: str) -> bytes:
        return base64.b64decode(string)
    
    def __decode(self, data: bytes) -> str: 
        return base64.b64encode(data).decode('utf-8')
    