import base64
from messages.common.Serializable import Serializable
from enum import Enum

class VerificationMessageData:
    def __init__(self, y, hash, b, prime):
        self.y = y
        self.hash = hash
        self.b = b
        self.prime = prime

class VerificationMessage(Serializable):
    YProperty = "y"
    HashProperty = "hash"
    BProperty = "b"
    PrimeProperty = "prime"

    def __init__(self, data):
        if (isinstance(data, VerificationMessageData)):
            self.y = data.y
            self.hash = data.hash
            self.b = data.b
            self.prime = data.prime

        elif (isinstance(data, dict)):
            hashData = data[VerificationMessage.HashProperty]
            hash = base64.b64decode(hashData)
            self.hash = hash 
            self.y = data[VerificationMessage.YProperty]
            self.b = data[VerificationMessage.BProperty]
            self.prime = data[VerificationMessage.PrimeProperty]
        else:
            self.y = -1
            self.hash = -1
            self.b = -1
            self.prime -1

    def to_map(self) -> dict:
        hash = base64.b64encode(self.hash).decode('utf-8')
        return {
            VerificationMessage.YProperty: self.y,
            VerificationMessage.HashProperty: hash,
            VerificationMessage.BProperty: self.b,
            VerificationMessage.PrimeProperty: self.prime
        }
    
class VerificationReponseMessage:
    YProperty = "y"

    def __init__(self, data):
        if (isinstance(data, int)):
            self.y = data
        elif (isinstance(data, dict)):
            self.y = data[VerificationMessage.YProperty]
        else:
            self.y = ""

    def toMap(self) -> dict:
        return {
            VerificationReponseMessage.YProperty: self.y,
        }
    
class VerificationStatus(Enum):
    PRE = 1
    SENT = 2
    POST = 3