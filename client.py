import socket
import threading
import sys
import config as cg
from message import UserLoginMessage, Serializable, SendAllMessage
import json

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
                
                client = Client(s)
                
                listener_thread = threading.Thread(target=client.listen_for_server)
                listener_thread.daemon = True
                listener_thread.start()
                
                client.main_loop()
                
        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server. Is it running?")
        except KeyboardInterrupt:
            print("\nForce quitting...")

if __name__ == "__main__":
    Driver()