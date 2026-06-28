import socket
import json
import threading
import config as cg
from messages.Serlializable import Serializable
from messages.ConnectionStatus import ConnectionStatus
from messages.SendTextMessage import SendTextMessage
from messages.UserLoginMessage import UserLoginMessage, UserLoginStatus, UserLoginMessageData
from messages.Common import Common
from abc import ABC, abstractmethod
import time

class ClientSupport(ABC):
    LOGIN_DELAY = 5

    def __init__(self, socket):
        self.__socket = socket
        self.__running = False
        self.__status = ConnectionStatus.UNVERIFIED

        self.__attempsLeft = 3
        self.__lastLoginAttempt: float = -1

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

    def __handleData(self, data: dict):
        print(f"[RECIVED] {data}")
        if (data[Serializable.ClassName] == UserLoginStatus.__name__):
            status = data[UserLoginStatus.StatusProperty]
            self.__status = ConnectionStatus[status]
        
    def __listenToServer(self):
        try:
            while self.__running:
                data = self.__socket.recv(Common.RECV_SIZE)
                print("data", data)
                if not data:
                    print("Disconnect")
                    self._serverDisconnect()
                    break
                else:
                    decoded = data.decode(Common.ENCODE_TYPE)
                    print("Decoded", decoded)
                    receivedData: dict = json.loads(decoded)
                    print("Handleing", receivedData)
                    self.__handleData(receivedData)
        except Exception as ex:
            print(f"[ERROR] {ex}")
            self._terminate()

    def _sendToServer(self, serializable: Serializable):
        classMap = {
            Serializable.ClassName: type(serializable).__name__
        }
        finalMap = serializable.toMap() | classMap
        jsonData = json.dumps(finalMap).encode(Common.ENCODE_TYPE)
        self.__socket.sendall(jsonData)
        print("sent", jsonData)

    def __mainLoop(self) -> None:
        while self.__running:
            if self.__status == ConnectionStatus.UNVERIFIED:
                if time.time() - self.__lastLoginAttempt >= ClientSupport.LOGIN_DELAY and self.__attempsLeft > 0:
                    self.__verificationFunc()
                    self.__lastLoginAttempt = time.time()
                    self.__attempsLeft -= 1
                elif self.__attempsLeft <= 0:
                    print("Failed login")
                    self._terminate()
            elif self.__status == ConnectionStatus.VERIFIED:
                self.__verifiedFunc()
            else:
                pass

    def __verificationFunc(self):
        name = input("Name: ")
        passowrd = input("Password: ")
        msg = UserLoginMessage(UserLoginMessageData(name, passowrd))
        self._sendToServer(msg)

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