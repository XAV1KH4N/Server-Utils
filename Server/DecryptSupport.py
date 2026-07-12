import os
from RSA.RSAPublic import RSAPublicKeyReader
from RSA.RSAKeyPairGen import RSAKeyPairGen
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives import hashes
from messages.VerificationMessage import VerificationMessage, VerificationStatus

class EncryptionSupport:
    def toBytes(y: int) -> bytes:
        return y.to_bytes((y.bit_length() + 7) // 8, byteorder='big')

class DecryptSupport:
    Y = 5073 ## This is not the secret number

    def __init__(self):       
        self.__publicHandler = self.__loadPublicHandler() 
        self.__status = VerificationStatus.PRE
    
    def hash(self, y: bytes):
        return Hash.hash(hashes.SHA256(), y)
    
    def verify(self, msg: VerificationMessage) -> bool:
        verified = self.verifySignature(msg.y, msg.hash)
        return verified

    def verifySignature(self, y: int, cipherHash) -> bool:
        b = EncryptionSupport.toBytes(y)
        return self.__publicHandler.verifyMessage(b, cipherHash)
    
    def sentMessage(self):
        self.__status = VerificationStatus.SENT

    def isSecure(self) -> bool:
        return self.__status == VerificationStatus.POST
    
    def __loadPublicHandler(self):
        if (not self.__fileExists(RSAKeyPairGen.PUBLIC_PATH)):
            raise Exception("Key Not Found")
            
        reader = RSAPublicKeyReader(RSAKeyPairGen.PUBLIC_PATH)
        return reader.handler()

    def __fileExists(self, path):
        return os.path.exists(path)
