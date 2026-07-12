from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class RSAPrivateHandler:
    def __init__(self, key):
        self.__private_key = key

    def decryptMessage(self, cipher: str):
        return self.__private_key.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
    
    def signMessage(self, msg: bytes):
        return self.__private_key.sign(
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

class RSAPrivateKeyReader:
    def __init__(self, path):
        self.__path = path

    def handler(self) -> RSAPrivateHandler: 
        key = self.__loadPrivatekey()
        return RSAPrivateHandler(key)
        
    def __loadPrivatekey(self):
        with open(f"{self.__path}", 'rb') as pem_in:
            pemlines = pem_in.read()
            key = load_pem_private_key(pemlines, None, default_backend())
            return key        

class RSAPrivateKeyWriter:
    def __init__(self, path):
        self.__path = path

    def savePrivateKey(self, private_key):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(f"{self.__path}", 'wb') as pem_out:
            pem_out.write(pem)