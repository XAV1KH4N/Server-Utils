import socket
import config as cg

class Driver:
    def __init__(self):
        self.start()
        print("Ending...")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((cg.Config.HOST, cg.Config.PORT))
            s.listen()
            print(f'Listening on {cg.Config.HOST}:{cg.Config.PORT}')
            conn, addr = s.accept()
            with conn:
                print(f'Connected to {addr}')
                while True:
                    data = conn.recv(1024)
                    print(f'Received {data}')
                    if not data:
                        break
                    conn.sendall(data)
            s.close

class Server:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        print("Innit")

    def listen(self):
        with self.conn:
            try:
                print(f'Connected to {self.addr}')
                run = True
                while run:
                    data = self.conn.recv(1024)
                    print(f'Recieved {data}')
                    self.conn.sendall(data)
            except KeyboardInterrupt:
                print("Forced Exit")

    def handleData(self, data):
        pass

if (__name__ == "__main__"):
    Driver()
