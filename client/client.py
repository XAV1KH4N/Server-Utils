from abc import ABC, abstractmethod
from client.connections.ServerConnectionHandler import ServerConnectionHandler
from client.events.ServerMessageEvent import ServerMessageEvent
from common.events import KeyExchangeRecievedEvent
from common.events.EventBus import EventBus
from common.events.Events import Event, EventHandler
from common.logging.Logger import Logger
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage
from messages.common.Serializable import Serializable
from messages.common.MessageBuilder import MessageBuilder

class MessageHandler(EventHandler, Logger):
    def __init__(self, event_bus: EventBus):
        self.__message_builder = MessageBuilder()
        self.event_bus = event_bus
        self.event_bus.subscribe(self)

    def on_change(self, event: Event):
        match event:
            case ServerMessageEvent():
                self.__handle__server_msg(event.getMsg())
            case _ : 
                pass

    def __handle__server_msg(self, msg: Serializable) -> None:
        rebuilt_msg = self.__message_builder.extract_message(msg)
        match rebuilt_msg:
            case KeyExchangeInitMessage():
                self.event_bus.publish(KeyExchangeRecievedEvent(msg))
            case _ : 
                self.logWarning("Unexpected server message", msg.to_map())

class Client(ABC):
    def __init__(self):
        self._event_bus = EventBus()
        self._connection_handler = ServerConnectionHandler()

    def start(self):
        self._connection_handler.with_connection(self.main_loop)

    @abstractmethod
    def main_loop(self) -> None:
        pass

class TestClient(Client):

    def main_loop(self):
        while True:
            pass

class TestClientDriver:
    def start():
        TestClient().start()

if __name__ == "__main__":
    TestClientDriver.start()