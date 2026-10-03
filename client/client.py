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

class Client(ABC, Logger):
    def __init__(self):
        self._event_bus = EventBus()
        self._connection_handler: ServerConnectionHandler = self.create_connection_handler()

    def start(self):
        self._connection_handler.with_connection(self.main_loop)

    def create_connection_handler(self) -> None:
        self.logWarning("Using default connection handler")
        return ServerConnectionHandler(self._event_bus, MessageBuilder())

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