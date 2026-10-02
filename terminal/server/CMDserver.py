from Server.connections.ConnectionHandler import ConnectionHandler
from Server.handler.KeyExchangeHandler import KeyExchangeHandler
from Server.serverModule import ServerBuilder, Server
from common.events.EventBus import EventBus
from common.events.Events import Event
from common.logging.Logger import Logger
from messages.common.TextMessage import TextMessage
from terminal.server.CMDMessageHandler import BroadcastAllEvent, CMDMessageHandler

class CMDServer(Server):
    def on_change(self, event: Event) -> bool:
        handled = super().on_change(event)
        if (handled):
            return True

        match event:
            case _:
                self.logError("Unhandled event for server (CMD)")
                return False
        return True

class CMDServerBuilder(ServerBuilder):
    def build(self) -> Server:
        event_bus = EventBus()
        msg_handler = CMDMessageHandler(event_bus)
        conn_handler = CMDConnectionHandler(event_bus)
        key_handler = KeyExchangeHandler(event_bus)
        return Server(msg_handler, conn_handler, key_handler, event_bus)

class CMDServerDriver:
    def start():
        print("Starting")
        server = CMDServerBuilder().build()
        server.start()

class CMDConnectionHandler(ConnectionHandler, Logger):

    def on_change(self, event: Event):
        super().on_change(event)

        if isinstance(event, BroadcastAllEvent):
            id = event.get_id()
            text = event.get_text()
            msg = TextMessage(text)
            self.logInfo("Sending to client")
            for conn in self._connections:
                if not conn.is_id(id):
                    self._connections[conn].send_to_client(msg)

if __name__ == "__main__":
    CMDServerDriver.start()