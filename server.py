import socket
import json
import threading
from common.logging.Logger import Logger
import config as cg
from messages.common.Serializable import Serializable
from messages.ConnectionStatus import ConnectionStatus
from messages.SendTextMessage import SendTextMessage
from messages.UserLoginMessage import UserLoginMessage, UserLoginStatus
from messages.VerificationMessage import VerificationReponseMessage
from messages.Common import Common
from abc import ABC, abstractmethod
from RSA.RSAKeyPairGen import *
from RSA.RSAPrivate import *
from RSA.RSAPublic import *
from Server.EncryptSupport import *

class ServerSupport(ABC, Logger):
    def __init__(self, encrypt: EncrpytConnectionSupport):
        self._status = ConnectionStatus.UNVERIFIED 
        self.__attemptsLeft = 3
        self.__encrypt = encrypt
    
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

        #sender = threading.Thread(target=self.__sendLoop)
        #sender.daemon = True
        #sender.start()

    def __updateState(self, newState: ConnectionStatus):
        self._status = newState
        self._send_to_client(UserLoginStatus(newState))
        
    def __handlePendingData(self, data: dict):
        if (not self.__encrypt.isSecure()):
            if (data[Serializable.ClassName] == VerificationReponseMessage.__name__):
                msg = VerificationReponseMessage(data)
                self.__encrypt.markPost(msg.y)
                self.logDebug("K", self.__encrypt.k())
            else:
                self.logWarning("Msg not expected")


        elif (data[Serializable.ClassName] == UserLoginMessage.__name__):
            name = data[UserLoginMessage.NameProperty]
            password = data[UserLoginMessage.PassProperty]
            if name == "xavi" and password == "1234":
                self.logInfo("Login Successful")
                self.__updateState(ConnectionStatus.VERIFIED)
            else:
                self.logInfo("Login Failed")
                self.__updateState(ConnectionStatus.UNVERIFIED)
                self.__attemptsLeft -= 1

    def __listen(self):
        with self._getConn():
            self.logDebug("With Connection")
            try:
                self.__sendVerificationMessage()

                while self._isRunning():
                    data = self._conn.recv(1024)
                    self.logDebug("** Data", data)
                    if not data:
                        self._disconnected()
                    else:
                        recievedData: dict = json.loads(data.decode(Common.ENCODE_TYPE))
                        self.logDebug("Status", self._status)
                        if self._status == ConnectionStatus.UNVERIFIED:
                            self.logDebug("pending data")
                            self.__handlePendingData(recievedData)
                        elif self._status == ConnectionStatus.VERIFIED:
                            self.logInfo(f"Recieved: {recievedData}")
                            self._handleData(recievedData)
                    self.__postCheck()
                            
            except KeyboardInterrupt as e:
                self.logError(f"\nConnection error with {self._getAddr()}: {e}")
            finally:
                self._running = False
            
    def __postCheck(self):
        if (self.__attemptsLeft <= 0):
            self.__updateState(ConnectionStatus.BLOCKED)
        
        if (self._status == ConnectionStatus.BLOCKED):
            self._running = False

    def __sendLoop(self):
        self.__sendVerificationMessage()
        
        while self._running:
            try:
                msg = input(f"Send to {self._getAddr()} -> ")
                if msg.strip() and self._running:
                    self.logInfo(f"Sending {msg}")
                    self._sendTextToClient(msg)
            except Exception as e:
                break                

    def __sendVerificationMessage(self):
        msg = self.__encrypt.intialMessage()
        self.logDebug(msg)
        self.logDebug(msg.to_map())
        self._send_to_client(msg)

    def _send_to_client(self, msg: Serializable):
        classMap = {
            Serializable.ClassName: type(msg).__name__
        }
        finalMap = msg.to_map() | classMap
        jsonData = json.dumps(finalMap).encode(Common.ENCODE_TYPE)
        self._getConn().sendall(jsonData)

    def _sendTextToClient(self, string: str):
        msg = SendTextMessage(string)
        self._send_to_client(msg)

class TestServerSupport(ServerSupport): # Multiple server connection handlers, but only one "server", it will just have lots of conenctions. Gotta manage this
    def __init__(self, conn, addr, encrypt: EncryptSupport):
        self._conn = conn
        self._addr = addr
        self._running = True
        encrypt = EncrpytConnectionSupport(encrypt)
        super().__init__(encrypt)

    ## Verify the client, then move connection to another support class once verified?
    # Once connected, start verification 

    def _handleData(self, data: dict):
        className = data[Serializable.ClassName]
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
        self.logError(f"\n[DISCONNECTED] Client {self._getAddr()} disconnected")
        self._running = False

class ConnectionManager(Logger):
    def __init__(self):
        self.connections = []
        self.__encrypt = EncryptSupport()
    
    def enqueue(self, conn, addr):
        self.logInfo(f"\n[NEW CONNECTION] {addr} connected.")
        handler = TestServerSupport(conn, addr, self.__encrypt)
        self.connections.append(handler)
        handler.run()

class Server(Logger):
    def __init__(self):
        self.manager = ConnectionManager()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((cg.Config.HOST, cg.Config.PORT))
            s.listen()

            self.logInfo(f'[SERVER STARTED] Always listening on {cg.Config.HOST}:{cg.Config.PORT}...')

            while True:
                try:
                    conn, addr = s.accept() 
                    self.manager.enqueue(conn, addr)
                except KeyboardInterrupt:
                    self.logInfo("\n[SHUTTING DOWN] Server shutting down manually.")
                    break
                except Exception as e:
                    self.logError(f"[SERVER ERROR] {e}")
                    break

if __name__ == "__main__":
    Server().run()