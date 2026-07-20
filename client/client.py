from abc import ABC, abstractmethod
from client.connections.ServerConnectionHandler import ServerConnectionHandler
from common.events.Events import Event, EventOrigin, EventPublisher
from common.logging.Logger import log
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage
from client.connections.ServerConnectionHandler import ServerMessageEvent
from messages.common.Serializable import Serializable

class MessageHandler(EventPublisher):
    def handle_event(self, event: Event):
        match event.get_origin():
            case EventOrigin.COMMUNICATION_HANDLER:
                self.__handle_event(event)
            case _ : 
                log("Unexpected message")

    def __handle_event(self, event: Event) -> None:
        match event:
            case ServerMessageEvent():
                self.__handle__server_msg(event.getMsg())
            case _ : 
                log("Unexpected message recieved")

    def __handle__server_msg(self, msg: Serializable) -> None:
        match msg:
            case KeyExchangeInitMessage():
                print("Recieved Key Exchange")
                pass
            case _ : 
                log("Unexpected server message")

class Client(ABC):
    def __init__(self):
        self.__connection_handler = ServerConnectionHandler()

    def start(self):
        self.__connection_handler.initiate_connection()

    @abstractmethod
    def main_loop(self) -> None:
        pass

class CMDClient(Client):

    def main_loop(self):
        while True:
            pass

class ClientDriver:
    def start():
        CMDClient().start()

if __name__ == "__main__":
    ClientDriver.start()