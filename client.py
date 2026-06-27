import socket
import threading
import sys
import config as cg
from message import UserLoginMessage, Serializable, SendAllMessage, SendTextMessage
import json
from abc import ABC, abstractmethod

class Common:
    RECV_SIZE = 1024
    ENCODE_TYPE = "utf-8"

# Tests for this

class ClientSupport(ABC):
    def __init__(self, socket):
        self.__socket = socket
        self.__running = False

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
        
    def __listenToServer(self):
        try:
            while self.__running:
                data = self.__socket.recv(Common.RECV_SIZE)
                print("data", data)
                if not data:
                    print("Disconnect")
                    self.__serverDisconnect()
                    break
                else:
                    decoded = data.decode(Common.ENCODE_TYPE)
                    print("Decoded", decoded)
                    receivedData: dict = json.loads(decoded)
                    print("Handleing", receivedData)
                    self.__handleData(receivedData)
        except Exception as ex:
            print(f"[ERROR] {ex}")
            self.__terminate()

    def _sendToServer(self, serializable: Serializable):
        classMap = {
            Serializable.ClassName: type(serializable).__name__
        }
        finalMap = serializable.toMap() | classMap
        jsonData = json.dumps(finalMap).encode(Common.ENCODE_TYPE)
        self.__socket.sendall(jsonData)

    def __mainLoop(self) -> None:
        while self.__running:
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
            (2) Send to all clients
            (3) Exit  
            """)
        
    def _handleChoice(self, choice: str) -> None:
        if (choice == "1"):
            self.__handleSendMessage()
        elif (choice == "2"):
            pass
        elif (choice == "3"):
            pass
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
            print("[ERROR] Could not connect to server. Is it running?")
        except KeyboardInterrupt:
            print("\nForce quitting...")

if __name__ == "__main__":
    Driver()