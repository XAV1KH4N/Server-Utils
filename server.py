import socket
import json
import threading
import config as cg
from message import UserLoginMessage, Serializable, SendAllMessage, SendTextMessage
from client import Common
from abc import ABC, abstractmethod

class ServerSupport(ABC):
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
        listener = threading.Thread(target=self.__listen)
        listener.daemon = True
        listener.start()

        sender = threading.Thread(target=self.__sendLoop)
        sender.daemon = True
        sender.start()

    def __listen(self):
        with self._getConn():
            try:
                while self._isRunning():
                    data = self._conn.recv(1024)
                    if not data:
                        self._disconnected()
                    else:
                        recievedData: dict = json.loads(data.decode(Common.ENCODE_TYPE))
                        print(f"Recieved: {recievedData}")
                        self._handleData(recievedData)
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

    def _sendTextToClient(self, string: str):
        msg = SendTextMessage(string)

        classMap = {
            Serializable.ClassName: type(msg).__name__
        }

        finalMap = msg.toMap() | classMap
        jsonData = json.dumps(finalMap).encode(Common.ENCODE_TYPE)
        self._getConn().sendall(jsonData)

class TestServerSupport(ServerSupport):
    def __init__(self, conn, addr):
        self._conn = conn
        self._addr = addr
        self._running = True

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

class ServerDriver:
    def __init__(self):
        self.start_server()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((cg.Config.HOST, cg.Config.PORT))
            s.listen()
            print(f'[SERVER STARTED] Always listening on {cg.Config.HOST}:{cg.Config.PORT}...')

            try:
                conn, addr = s.accept() 
                print(f"\n[NEW CONNECTION] {addr} connected.")
                    
                handler = TestServerSupport(conn, addr)
                handler.run()
                    
            except KeyboardInterrupt:
                print("\n[SHUTTING DOWN] Server shutting down manually.")
            except Exception as e:
                print(f"[SERVER ERROR] {e}")

if __name__ == "__main__":
    ServerDriver()