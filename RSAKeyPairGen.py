from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from RSAPublic import *
from RSAPrivate import *

class RSAKeyPairGen:
    PATH = "keys/"
    PRIVATE = "private"
    PUBLIC = "public"
    EXT = ".PEM"

    PUBLIC_PATH = f"{PATH}{PUBLIC}{EXT}"
    PRIVATE_PATH = F"{PATH}{PRIVATE}{EXT}"

    def __init__(self):
        self.__privateWriter = RSAPrivateKeyWriter(self.PRIVATE_PATH) 
        self.__publicWriter = RSAPublicKeyWriter(self.PUBLIC_PATH) 

    def refreshKeys(self):
        private = self.__createPrivateKey()
        public = private.public_key()

        self.__privateWriter.savePrivateKey(private)
        self.__publicWriter.savePublicKey(public)

    def __createPrivateKey(self):
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)
