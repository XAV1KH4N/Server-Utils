from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate a new elliptic curve key pair

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

#private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
public_key = private_key.public_key()

# Print the public and private keys
print(f'Private key: {private_key}')
print(f'Public key: {public_key}')
# Encrypt the message using the public key
message = b'The secret message no one should read'
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypting the message (=cyphertext) using your private key
decrypted_message = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Printing the original and decrypted secret message
print(f'Original message: {message}')
print(f'Decrypted message: {decrypted_message}')