import socket
import threading
import sys
import config as cg

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
                
                # Print the server's update immediately
                print(f"\n[SERVER UPDATE] {data.decode()}")
                # Print a fresh prompt marker so the user knows they can still type
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
                break  # Exit if the background thread found out the server died
                
            if choice == "1":
                self.handle_send()
            elif choice == "2":
                self.handle_exit()
                break
            else:
                print("Invalid choice. Try again.")

    def print_menu(self):
        print("""
        ### Client Menu ###
        (1) Send Message
        (2) Exit  
        """)
        
    def handle_send(self):
        print("\nEnter your message to the server:")
        msg = input(": ")
        if msg.strip():
            try:
                self.socket.sendall(msg.encode())
            except Exception as e:
                print(f"[ERROR] Failed to send message: {e}")
                self.running = False

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
                
                # Start the server listener thread in the background
                listener_thread = threading.Thread(target=client.listen_for_server)
                listener_thread.daemon = True
                listener_thread.start()
                
                # Keep the main thread running the menu loop
                client.main_loop()
                
        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server. Is it running?")
        except KeyboardInterrupt:
            print("\nForce quitting...")

if __name__ == "__main__":
    Driver()