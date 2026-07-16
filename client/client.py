from abc import ABC, abstractmethod
from connections.ServerConnectinoHandler import ServerConnectionHandler
from common.events.Events import Event, EventDesitination, EventHandler, EventOrigin, EventPublisher
from common.logging.Logger import log

class MessageHandler(EventPublisher):
    def handle_event(self, event: Event):
        match event.getOrigin():
            case EventOrigin.COMMUNICATION_HANDLER:
                self.__handle_server_message(event)
            case _ : 
                log("Unexpected message")

    def __handle_server_message(self, event: Event):
        match event:
            case 
            case _ : 
                log("Unexpected message recieved")



class Client(ABC):
    def __init__(self):
        self.__connection_handler = ServerConnectionHandler()

    def start(self):
        self.__connection_handler.run_in_background()
        self.__verification_loop()

    def __verification_loop(self) -> None:
        # Verify, then move to main loop
        is_verified = False
        while not is_verified:
            # wait for intial message
            pass

    @abstractmethod
    def main_loop(self) -> None:
        pass

class CMDClient(Client):
    def main_loop(self):
        while True:
            pass

class ClientDriver:
    def start():
        Client().start()

if __name__ == "__main__":
    ClientDriver.start()