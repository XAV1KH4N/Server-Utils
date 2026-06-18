import socket
import threading
import config as cg

class ClientHandler:
    """Manages a single client connection's lifecycle on its own thread."""
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.running = True

    def start(self):
        # Spin up a thread to listen for data from this specific client
        listener = threading.Thread(target=self.listen)
        listener.daemon = True
        listener.start()

        # Spin up a thread to allow server terminal inputs to ping this client
        sender = threading.Thread(target=self.send_loop)
        sender.daemon = True
        sender.start()

    def listen(self):
        with self.conn:
            try:
                while self.running:
                    data = self.conn.recv(1024)
                    if not data:
                        print(f"\n[DISCONNECTED] Client {self.addr} disconnected.")
                        break
                    print(f'\n[{self.addr}] Received: {data.decode()}')
            except Exception as e:
                print(f"\n[ERROR] Connection error with {self.addr}: {e}")
            finally:
                self.running = False

    def send_loop(self):
        while self.running:
            try:
                msg = input(f"Send to {self.addr} -> ")
                if msg.strip() and self.running:
                    self.conn.sendall(msg.encode())
            except Exception as e:
                break


class ServerDriver:
    def __init__(self):
        self.start_server()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((cg.Config.HOST, cg.Config.PORT))
            s.listen()
            print(f'[SERVER STARTED] Always listening on {cg.Config.HOST}:{cg.Config.PORT}...')

            # This loop ensures the server never exits and is ALWAYS ready for a new connection
            while True:
                try:
                    # Blocks here until a client shows up, but instantly loops back once one does!
                    conn, addr = s.accept() 
                    print(f"\n[NEW CONNECTION] {addr} connected.")
                    
                    # Create a handler and kick off its individual threads
                    handler = ClientHandler(conn, addr)
                    handler.start()
                    
                except KeyboardInterrupt:
                    print("\n[SHUTTING DOWN] Server shutting down manually.")
                    break
                except Exception as e:
                    print(f"[SERVER ERROR] {e}")

if __name__ == "__main__":
    ServerDriver()