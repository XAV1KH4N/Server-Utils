class EncryptUtils:
    ENCODE_TYPE = "utf-8"
    
    KEY_SIZE = 32
    BLOCK_SIZE = 16

    def to_bytes(y: int) -> bytes:
        return y.to_bytes((y.bit_length() + 7) // 8, byteorder='big')