from messages.VerificationMessage import VerificationMessage
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class DiffeHellam:
    def __init__(self, yThis):
        self.yThis = yThis

    def updateFromInts(self, b, prime):
        #self.y = y
        self.b = b
        self.p = prime

    def updateY(self, y):
        self.y = y

    def updateFromMessage(self, msg: VerificationMessage):
        self.y = msg.y
        self.b = msg.b
        self.p = msg.prime

    def k(self): 
        return pow(self.y, self.yThis, self.p)

    def yMod(self):
        return (self.b ** self.yThis) % self.p
    

class SymetricEncryptionSupport:    
    def __init__(self, key: int):
        #self.key = base64.b64decode(f"{key}")
        #self.key = base64.b64decode("7Y/Ycbyw407VkBBKh7veNkpk9uBHg+h4YT+PTkcIcY8=")
        self.backend = default_backend()
        self.key = os.urandom(32)
        self.iv = os.urandom(16)

    def encrypt(self, data: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(b"a secret message") + encryptor.finalize()
        return ct

    def decrypt(self, text: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        return decryptor.update(text) + decryptor.finalize()
