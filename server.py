import socket
import json
import threading
import config as cg
from message import UserLoginMessage, Serializable, SendAllMessage, SendTextMessage, ConnectionStatus, UserLoginStatus
from client import Common
from abc import ABC, abstractmethod

class ServerSupport(ABC):
    def __init__(self):
        self._status = ConnectionStatus.PENDING
        
    @abstractmethod
    def _getConn(self):
        """Client connection stream"""

    @abstractmethod
    def _getAddr(self):
        """Bind addresss"""

    @abstractmethod
    def _isRunning(self) -> bool:
        """Running state"""
    
    @abstractmethod
    def _handleData(self, data: dict):
        """Handle data from client"""

    def _disconnected(self):
        """Disconnection from client"""

    def run(self):
        # verifiy before we start this
        # 1. Pending
        # 2. Recieve message
        # 3. verified
        # 4. Start loop

        listener = threading.Thread(target=self.__listen)
        listener.daemon = True
        listener.start()

        sender = threading.Thread(target=self.__sendLoop)
        sender.daemon = True
        sender.start()

    def __handlePendingData(self, data: dict):
        if (data[Serializable.ClassName] == UserLoginMessage.__name__):
            name = data[UserLoginMessage.NameProperty]
            password = data[UserLoginMessage.PassProperty]
            if name == "xavi" and password == "1234":
                self._status = ConnectionStatus.VERIFIED
                print("Login Successful")
                self._sendToClient(UserLoginStatus(ConnectionStatus.VERIFIED))
            else:
                self._status = ConnectionStatus.FAILED
                print("Login Failed")

    def __listen(self):
        with self._getConn():
            try:
                while self._isRunning():
                    data = self._conn.recv(1024)
                    if not data:
                        self._disconnected()
                    else:
                        recievedData: dict = json.loads(data.decode(Common.ENCODE_TYPE))
                        if self._status == ConnectionStatus.PENDING:
                            self.__handlePendingData(recievedData)
                        elif self._status == ConnectionStatus.VERIFIED:
                            print(f"Recieved: {recievedData}")
                            self._handleData(recievedData) ## Need to send message to client to express the conenction state

            except KeyboardInterrupt as e:
                print(f"\n[ERROR] Connection error with {self._getAddr()}: {e}")
            finally:
                self._running = False

    def __sendLoop(self):
        while self._running:
            try:
                msg = input(f"Send to {self._getAddr()} -> ")
                if msg.strip() and self._running:
                    print(f"Sending {msg}")
                    self._sendTextToClient(msg)
            except Exception as e:
                break                

    def _sendToClient(self, msg: Serializable):
        classMap = {
            Serializable.ClassName: type(msg).__name__
        }
        finalMap = msg.toMap() | classMap
        jsonData = json.dumps(finalMap).encode(Common.ENCODE_TYPE)
        self._getConn().sendall(jsonData)

    def _sendTextToClient(self, string: str):
        msg = SendTextMessage(string)
        self._sendToClient(msg)

class TestServerSupport(ServerSupport): # Multiple server connection handlers, but only one "server", it will just have lots of conenctions. Gotta manage this
    def __init__(self, conn, addr):
        self._conn = conn
        self._addr = addr
        self._running = True
        super().__init__()

    ## Verify the client, then move connection to another support class once verified?
    # Once connected, start verification 

    def _handleData(self, data: dict):
        className = data[Serializable.ClassName]
        print("Class name", className)
        if (className == SendTextMessage.__name__):
            textMsg = SendTextMessage(data)
            text = textMsg.getText()
            print(f"Text {text}")
        else:
            print("Could not process")

    def _getConn(self):
        return self._conn

    def _getAddr(self):
        return self._addr
    
    def _isRunning(self) -> bool:
        return self._running
    
    def _disconnected(self):
        print(f"\n[DISCONNECTED] Client {self._getAddr()} disconnected")
        self._running = False

class ConnectionManager:
    def __init__(self):
        self.connections = []
    
    def enqueue(self, conn, addr):
        print(f"\n[NEW CONNECTION] {addr} connected.")
        handler = TestServerSupport(conn, addr)
        self.connections.append(handler)
        handler.run()

class Server:
    def __init__(self):
        self.manager = ConnectionManager()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((cg.Config.HOST, cg.Config.PORT))
            s.listen()

            print(f'[SERVER STARTED] Always listening on {cg.Config.HOST}:{cg.Config.PORT}...')

            while True:
                try:
                    conn, addr = s.accept() 
                    self.manager.enqueue(conn, addr)
                except KeyboardInterrupt:
                    print("\n[SHUTTING DOWN] Server shutting down manually.")
                    break
                except Exception as e:
                    print(f"[SERVER ERROR] {e}")
                    break

if __name__ == "__main__":
    Server().run()