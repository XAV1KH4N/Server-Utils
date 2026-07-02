from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

class RSAPublicHandler:
    def __init__(self, key):
        self.__public_key = key

    def decryptMessage(self, cipher: str):
        return self.__public_key.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
    
    def encryptMessage(self, msg: str):
        return self.__publicKey.encrypt(
            msg.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
class RSAPublicKeyReader:
    def __init__(self, path):
        self.__path = path

    def handler(self) -> RSAPublicHandler: 
        key = self.__loadPublickey()
        return RSAPublicHandler(key)
        
    def __loadPublickey(self):
        with open(f"{self.__path}", 'rb') as pem_in:
            pemlines = pem_in.read()
            key = load_pem_public_key(pemlines, None, default_backend())
            return key      
        
class RSAPublicKeyWriter:
    def __init__(self, path):
        self.__path = path

    def savePublicKey(self, publicKey):
        pem = publicKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(f"{self.__path}", 'wb') as pem_out:
            pem_out.write(pem)