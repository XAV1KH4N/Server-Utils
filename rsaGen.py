from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
from RSA.RSAPrivate import *
from RSA.RSAPublic import *
from RSA.RSAKeyPairGen import RSAKeyPairGen
from Server.EncryptSupport import *
from Server.DecryptSupport import *

## Note, you can make a private key from a public key, client should only ge the public
class RSAGen:
    PUBLIC_EXPONENT = 65537
    KEY_SIZE = 2048

    def __init__(self, key = None):
        if (key != None):
            self.__privateKey = key
        else:
            self.__privateKey = self.__createPrivateKey()

        self.__publicKey = self.__privateKey.public_key()

    def getPrivateKey(self):
        return self.__privateKey

    def getPublicKey(self):
        return self.__publicKey
    
    def encryptMessage(self, msg: str):
        return self.__publicKey.encrypt(
            msg.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def decryptMessage(self, cipher: str):
        return self.__privateKey.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

    def __createPrivateKey(self):
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
# Servers Private Key - Persisted
# Servers Public Key - Persisted
# Large number - Persisted

# Large number -> Hash

# Hash Y (Normal function)
# Sign Hash

### ---

# Client gets signed Hash Y and Y
# Verify signed Y (Should decrypt, then it should match Sign(Y))
# If so all good

class RSAKeyPersister:
    PATH = "keys/"
    PRIVATE = "private"
    PUBLIC = "public"
    EXT = ".PEM"

    def refreshKeys(self):
        gen = RSAGen()
        private = gen.getPrivateKey()
        self.savePrivateKey(private)
    
    def savePrivateKey(self, pk):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(f"{RSAKeyPersister.PATH}{RSAKeyPersister.PRIVATE}{RSAKeyPersister.EXT}", 'wb') as pem_out:
            pem_out.write(pem)

    def loadPrivatekey(self):
        with open(f"{RSAKeyPersister.PATH}{RSAKeyPersister.PRIVATE}{RSAKeyPersister.EXT}", 'rb') as pem_in:
            pemlines = pem_in.read()
            private_key = load_pem_private_key(pemlines, None, default_backend())
            return private_key

class RSAKeyPersister:
    PATH = "keys/"
    PRIVATE = "private"
    PUBLIC = "public"
    EXT = ".PEM"

    def refreshKeys(self):
        gen = RSAGen()
        private = gen.getPrivateKey()
        self.savePrivateKey(private)
    
    def savePrivateKey(self, pk):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(f"{RSAKeyPersister.PATH}{RSAKeyPersister.PRIVATE}{RSAKeyPersister.EXT}", 'wb') as pem_out:
            pem_out.write(pem)

    def loadPrivatekey(self):
        with open(f"{RSAKeyPersister.PATH}{RSAKeyPersister.PRIVATE}{RSAKeyPersister.EXT}", 'rb') as pem_in:
            pemlines = pem_in.read()
            private_key = load_pem_private_key(pemlines, None, default_backend())
            return private_key

class Driver:
    def testMsg(self):
        gen = RSAGen()
        msg = input(": ")
        cipher = gen.encryptMessage(msg)
        print(f'Cipher message: {cipher}')
        dmsg = gen.decryptMessage(cipher)
        print(f'Decrypted message: {dmsg}')

    def testWrite(self):
        writer = RSAKeyPersister()
        writer.refreshKeys()

    def testRead(self):
        writer = RSAKeyPersister()
        key = writer.loadPrivatekey()

        gen = RSAGen(key)
        msg = input(": ")
        cipher = gen.encryptMessage(msg)
        print(f'Cipher message: {cipher}')
        dmsg = gen.decryptMessage(cipher)
        print(f'Decrypted message: {dmsg}')

    def testPublicRead(self):
        privatePath = "keys/private.PEM"
        publicPath = "keys/public.PEM"

        privateReader = RSAPrivateKeyReader(privatePath)
        privateHandler = privateReader.handler()

        publicReader = RSAPublicKeyReader(publicPath)
        publicHandler = publicReader.handler()

        msg = input(": ")
        cipher = privateHandler.encryptMessage(msg)
        print(f'Cipher message: {cipher}')
        
        dmsg = publicHandler.decryptMessage(cipher)
        print(f'Decrypted message: {dmsg}')

    def testRefresh(self):
        gen = RSAKeyPairGen()
        gen.refreshKeys()

    def testHash(self):
        enc = EncryptSupport()
        signature = enc.signHash()

        dec = DecryptSupport()
        bs = EncryptSupport.Y_Bytes()
        b = dec.verifySignature(bs, signature)

        print("Verified", b)

    def testFailedMessageHash(self):
        enc = EncryptSupport()
        signature = enc.signHash()

        dec = DecryptSupport()
        bs = EncryptSupport.To_Bytes(1032)
        b = dec.verifySignature(bs, signature)

        print("Failed Verification", b)


    def testFailedSignatureHash(self):
        enc = EncryptSupport()

        bx = EncryptSupport.To_Bytes(1032)
        wrongSignature = enc.signMsgHash(bx)

        dec = DecryptSupport()
        bs = EncryptSupport.Y_Bytes()

        b = dec.verifySignature(bs, wrongSignature)

        print("Failed Verification", b)


if __name__ == "__main__":
    driver = Driver()
    driver.testHash()
    driver.testFailedMessageHash()
    driver.testFailedSignatureHash()
