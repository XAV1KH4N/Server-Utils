from abc import ABC, abstractmethod
from client.connections.ServerConnectionHandler import ServerConnectionHandler
from client.events.ServerMessageEvent import ServerMessageEvent
from common.events import KeyExchangeRecievedEvent
from common.events.Events import Event, EventOrigin, EventPublisher
from common.logging.Logger import log
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage
from messages.common.Serializable import Serializable
from messages.common.MessageBuilder import MessageBuilder
from messages.common.TextMessage import TextMessage

class MessageHandler(EventPublisher):
    def __init__(self):
        self.__message_builder = MessageBuilder()
        super().__init__()

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
        rebuilt_msg = self.__message_builder.extract_message(msg)
        print("Rebuilt Msg", rebuilt_msg)
        match rebuilt_msg:
            case KeyExchangeInitMessage():
                self.publish(KeyExchangeRecievedEvent(msg))
            case _ : 
                log("Unexpected server message")

class Client(ABC):
    def __init__(self):
        self._connection_handler = ServerConnectionHandler()

    def start(self):
        self._connection_handler.with_connection(self.main_loop)

    @abstractmethod
    def main_loop(self) -> None:
        pass

class CMDClient(Client):

    def main_loop(self):
        while True:
            self.__print_options()
            choice = input("-> ")
            valid, cleaned_choice = self.__validate_input(choice)
            if (valid):
                match cleaned_choice:
                    case 1:
                        self.__send_msg_to_server()
                    case _:
                        print("Missing implementation")

            else:
                print("Invalid Message")

    def __send_msg_to_server(self):
        msg = input("Enter Message: ")
        msg_data = TextMessage(msg)
        self._connection_handler.send_to_server_encrypted(msg_data)
        print("Encrypted + Sent")        

    def __validate_input(self, choice: str):
        valid = [1, 2, 3]
        try:
            i = int(choice)      
            return (i in valid), i
        except:
            return False, -1

    def __print_options(self) -> None:
        print('''
        Options ... 
           (1) Send to Server
           (2) Broadcast to clients
           (3) Terminate
        ''')

class ClientDriver:
    def start():
        CMDClient().start()

if __name__ == "__main__":
    ClientDriver.start()