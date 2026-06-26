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
                if not data:
                    self.__serverDisconnect()
                    break
                else:
                    receivedData: dict = json.loads(data.decode(Common.ENCODE_TYPE))
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

    
class Client:
    def __init__(self, sock):
        self.socket = sock
        self.running = True

    def listen_for_server(self):
        """Thread 1: Background listener that catches asynchronous server pings."""
        try:
            while self.running:
                data = self.socket.recv(1024)
                if not data:
                    print("\n[DISCONNECTED] Server closed the connection.")
                    self.running = False
                    break
                
                print(f"\n[SERVER UPDATE] {data.decode()}")
                print(": ", end="", flush=True)
                
        except Exception as e:
            if self.running:
                print(f"\n[ERROR] Connection lost: {e}")
        finally:
            self.running = False

    def main_loop(self):
        """Thread 2 (Main Thread): Handles the user menu navigation."""
        while self.running:
            self.print_menu()
            choice = input(": ").strip()
            
            if not self.running: 
                break  
                
            if choice == "1":
                self.handle_send()
            elif choice == "2":
                self.handle_exit()
                break
            elif choice == "3":
                self.handleSendAll()
            else:
                print("Invalid choice. Try again.")

    def print_menu(self):
        print("""
        ### Client Menu ###
        (1) Send Message
        (2) Exit  
        (3) Send to all clients
        """)

    def handleSendAll(self):
        print("Broadcast Message")
        msg = self.inputSendAllMessage()
        if msg != None:
            try:
                print(msg.toMap())
                self.send(msg)
            except Exception as e:
                print(f"[ERROR] Failed to send {e}")
                self.running = False        

    def send(self, serializable: Serializable):
        msg = serializable.toMap()  | {
            Serializable.ClassName: type(serializable).__name__
        }
        json_data = json.dumps(msg).encode("utf-8")
        self.socket.sendall(json_data)
        print("Send, ", self.running)
        
    def handle_send(self):
        print("\nEnter your message to the server:")
        usermsg = self.inputUserMessage()
        if usermsg != None:
            try:
                print(usermsg.toMap())
                self.send(usermsg)
            except Exception as e:
                print(f"[ERROR] Failed to send message: {e}")
                self.running = False

    def inputSendAllMessage(self):
        text = input("Message: ")

        if len(text) != 0:
            return SendAllMessage(text)
        else:
            return None

    def inputUserMessage(self) -> UserLoginMessage:
        username = input("Username: ")

        if len(username) != 0:
            return UserLoginMessage(username.strip())
        else:
            return None
            

    def handle_exit(self):
        print("Exiting client...")
        self.running = False


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
                
                #listener_thread = threading.Thread(target=client.listen_for_server)
                #listener_thread.daemon = True
                #listener_thread.start()
                
                #client.main_loop()
                
        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server. Is it running?")
        except KeyboardInterrupt:
            print("\nForce quitting...")

if __name__ == "__main__":
    Driver()