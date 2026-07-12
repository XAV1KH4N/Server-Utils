from messages.VerificationMessage import VerificationMessage

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
