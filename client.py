import socket
import json
import threading
import config as cg
from Server.DecryptSupport import DecryptSupport
from messages.common.Serlializable import Serializable
from messages.ConnectionStatus import ConnectionStatus
from messages.SendTextMessage import SendTextMessage
from messages.UserLoginMessage import UserLoginMessage, UserLoginStatus, UserLoginMessageData
from messages.VerificationMessage import VerificationMessage, VerificationReponseMessage
from messages.Common import Common
from RSA.DiffeHellam import DiffeHellam
from abc import ABC, abstractmethod
import time

class LoginSupport():
    MAX_ATTEMPTS = 3
    LOGIN_DELAY = 5

    def __init__(self):
        self.__status: ConnectionStatus = ConnectionStatus.UNVERIFIED 
        self.__attempsLeft: int = LoginSupport.MAX_ATTEMPTS
        self.__lastLoginAttempt: float = -1

    def failedLogin(self):
        self.__attempsLeft -= 1
        if (self.__attempsLeft < 0):
            self.__status == ConnectionStatus.BLOCKED

    def handleData(self, data: dict):
        print(f"[RECIVED] ## {data}")
        print(data, data[Serializable.ClassName], UserLoginStatus.__name__)
        if (data[Serializable.ClassName] == UserLoginStatus.__name__):
            status = data[UserLoginStatus.StatusProperty]
            self.__status = ConnectionStatus[status]
            self.failedLogin()
            print("Updated", status, self.__status)

    def buildLoginMessage(self) -> UserLoginMessage:
        name = input("Name: ")
        passowrd = input("Password: ")
        msg = UserLoginMessage(UserLoginMessageData(name, passowrd))
        self.__lastLoginAttempt = time.time()
        return msg
    
    def isDelayComplete(self) -> bool:
        return time.time() - self.__lastLoginAttempt >= LoginSupport.LOGIN_DELAY

    def hasAttemptsLeft(self) -> bool:
        return self.__attempsLeft > 0

    def canAttempt(self):
        return self.isDelayComplete() and self.hasAttemptsLeft()

    def isUnverified(self) -> bool:
        return self.__status == ConnectionStatus.UNVERIFIED
    
    def isVerified(self) -> bool:
        return self.__status == ConnectionStatus.VERIFIED
    
    def isBlocked(self) -> bool:
        return self.__status == ConnectionStatus.BLOCKED

class ClientSupport(ABC):
    def __init__(self, socket):
        self.__socket = socket
        self.__running = False
        self.__loginSupport = LoginSupport()
        self.__decrypt = DecryptSupport()
        self.__diffe = DiffeHellam(self.__decrypt.Y)
        
    @abstractmethod
    def _isOption(self, choice: str) -> bool:
        "Is input a valid selection"

    @abstractmethod
    def _printOptions(self) -> None:
        "Print all options"

    @abstractmethod
    def _handleChoice(self, choice: str) -> None:
        "handle the user input"

    def run(self):
        self.__running = True
                
        listener_thread = threading.Thread(target=self.__listenToServer)
        listener_thread.daemon = True
        listener_thread.start()

        self.__mainLoop()

    def _serverDisconnect(self):
        print("[DISCONNECTED] Serer closed the connection")
        self.__running = False

    def _terminate(self):
        print("[DISCONNECTED] Connection closed by client")
        self.__running = False

    def __handleUnverified(self, data: dict):
        msg = VerificationMessage(data)
        verified = self.__decrypt.verify(msg)
        if (verified):
            self.__diffe.updateFromMessage(msg)
            yMod = self.__diffe.yMod()
            self.__decrypt.sentMessage()
            response = VerificationReponseMessage(yMod)
            self._sendToServer(response)
        else:
            print("Unable to verify server")

    def __handleData(self, data: dict):
        print(f"[RECIVED]")# {data}")

        if (not self.__decrypt.isSecure()):
            self.__handleUnverified(data)
        else:
            self.__loginSupport.handleData(data)
        
    def __listenToServer(self):
        try:
            while self.__running:
                data = self.__socket.recv(Common.RECV_SIZE)
                if not data:
                    print("Disconnect")
                    self._serverDisconnect()
                    break
                else:
                    decoded = data.decode(Common.ENCODE_TYPE)
                    receivedData: dict = json.loads(decoded)
                    self.__handleData(receivedData)
        except KeyboardInterrupt as ex:
            print(f"[ERROR] {ex}")
            self._terminate()

    def _sendToServer(self, serializable: Serializable):
        classMap = {
            Serializable.ClassName: type(serializable).__name__
        }
        finalMap = serializable.to_map() | classMap
        jsonData = json.dumps(finalMap).encode(Common.ENCODE_TYPE)
        self.__socket.sendall(jsonData)

    def __mainLoop(self) -> None:
        while self.__running:
            if self.__loginSupport.isUnverified():
                if self.__loginSupport.canAttempt():
                    msg = self.__loginSupport.buildLoginMessage()
                    self._sendToServer(msg)
            elif self.__loginSupport.isVerified():
                self.__verifiedFunc()

            self.__postCheck()

    def __postCheck(self):
        if (self.__loginSupport.isBlocked()):
            self._terminate()

    def __verifiedFunc(self):
        self._printOptions()
        choice = input(": ")
        cleanedChoice, valid = self.__validate(choice)
        if (valid):
            self._handleChoice(cleanedChoice)
        else:
            print("[Error] Invalid input")

    def __validate(self, choice: str):
        cleaned = choice.strip()
        if len(cleaned) != 0 and self._isOption(cleaned):
            return cleaned, True
        else:
            return None, False 

class TestClient(ClientSupport):
    def __init__(self, socket):
        super().__init__(socket)    

    def _isOption(self, choice: str) -> bool:
        return choice in ["1", "2", "3"]

    def _printOptions(self) -> None:
        print("""
            ### Client Menu ###
            (1) Send Message
            (2) Exit  
            """)
        
    def _handleChoice(self, choice: str) -> None:
        if (choice == "1"):
            self.__handleSendMessage()
        elif (choice == "2"):
            self._terminate()
        else:
            print("Failed")

    def __handleSendMessage(self):
        str = input("Message: ")
        msg = SendTextMessage(str)
        self._sendToServer(msg)

class Driver:
    def __init__(self):
        self.start()

    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"Connecting to {cg.Config.HOST}:{cg.Config.PORT}...")
                s.connect((cg.Config.HOST, cg.Config.PORT))
                
                client = TestClient(s)
                client.run()
                
        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server")
        except KeyboardInterrupt:
            print("\nForce quitting...")

if __name__ == "__main__":
    Driver()