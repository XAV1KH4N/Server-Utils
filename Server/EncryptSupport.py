import os
from RSA.RSAPrivate import RSAPrivateKeyReader
from RSA.RSAKeyPairGen import RSAKeyPairGen
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives import hashes
from messages.VerificationMessage import VerificationMessage, VerificationMessageData, VerificationStatus
from RSA.DiffeHellam import DiffeHellam


class EncryptSupport:
    Y: int = 1031 # This is not the secret number // per connection
    P: int = 13
    B: int = 6

    def Y_Bytes():
        return EncryptSupport.To_Bytes(EncryptSupport.Y)
    
    def To_Bytes(y):
        return y.to_bytes((y.bit_length() + 7) // 8, byteorder='big')

    def __init__(self):
        self.__privateHandler = self.__loadPrivateHandler() 

    def y(self) -> bytes:
        return EncryptSupport.Y
    
    def prime(self) -> bytes:
        return EncryptSupport.P

    def b(self) -> int:
        return EncryptSupport.B

    def signHash(self):
        return self.__privateHandler.signMessage(EncryptSupport.Y_Bytes())
    
    def signMsgHash(self, msg: bytes):
        return self.__privateHandler.signMessage(msg)
         
    def __loadPrivateHandler(self):
        if (not self.__fileExists(RSAKeyPairGen.PRIVATE_PATH)):
            print("Generated")
            gen = RSAKeyPairGen()
            gen.refreshKeys()
            
        reader = RSAPrivateKeyReader(RSAKeyPairGen.PRIVATE_PATH)
        return reader.handler()

    def __fileExists(self, path):
        return os.path.exists(path)
    
class EncrpytConnectionSupport:
    def __init__(self, encrypt: EncryptSupport):       
        self.__status = VerificationStatus.PRE
        self.__encrypt = encrypt
        self.__diffe = DiffeHellam(self.__encrypt.y())

    def intialMessage(self):
        self.__status = VerificationStatus.SENT
        print("Creating Message")
        
        #y = self.__encrypt.y()
        self.__diffe.updateFromInts(self.__encrypt.b(), self.__encrypt.prime())
        y = self.__diffe.yMod()
        signature = self.__encrypt.signMsgHash(EncryptSupport.To_Bytes(y))
        b = self.__encrypt.b()
        p = self.__encrypt.prime()

        data = VerificationMessageData(y, signature, b, p)
        return VerificationMessage(data)
    
    def markPost(self, yOther: int):
        self.__diffe.updateY(yOther)
        self.__status = VerificationStatus.POST
    
    def isSecure(self) -> bool:
        return self.__status == VerificationStatus.POST
    
    def k(self):
        return self.__diffe.k()