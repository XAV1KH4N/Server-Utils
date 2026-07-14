from messages.VerificationMessage import VerificationMessage
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from cryptography.hazmat.primitives import padding

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
        self.backend = default_backend()
        self.key = key.to_bytes(32, byteorder='big')
        self.iv = os.urandom(16)

    def encrypt(self, data: bytes) -> bytes:
        padder = padding.ANSIX923(128).padder() 
        padData = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ct = encryptor.update(padData) + encryptor.finalize()
        return ct

    def decrypt(self, text: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        return decryptor.update(text) + decryptor.finalize()
