from common.EncyptUtils import EncryptUtils

class KeyExchangeSupport:
    def __init__(self):
        self._y = -1
        self._prime = -1
        self._base = -1

        self._other_Y = -1

    def set_up_this_y(self, y: int) -> None:
        self._y = y
    
    def set_up(self, base: int, prime: int):
        self._base = base
        self._prime = prime

    def set_up_other_y(self, other_Y: int) -> None:
        self._other_Y = other_Y

    def is_complete(self) -> bool:
        return self._other_Y != -1

    def Y(self) -> int:
        return pow(self._base, self._y, self._prime)
    
    def to_bytes(self, x: int) -> bytes:
        return EncryptUtils.to_bytes(x)
    
    def Y_bytes(self) -> bytes:
        return self.to_bytes(self.Y())
    
    def K(self) -> int:
        k =  pow(self._other_Y, self._y, self._prime)   
        print("k", k, "prime", self._prime, "base", self._base, "y", self._y, "Other y", self._other_Y)
        return k
