from Server.connections.ConnectionHandler import ConnectionHandler
from Server.handler.KeyExchangeHandler import KeyExchangeHandler
from Server.serverModule import ServerBuilder, Server
from common.events.Events import Event, EventOrigin
from messages.common.TextMessage import TextMessage
from teminal.server.CMDMessageHandler import BroadcastAllEvent, CMDMessageHandler

class CMDServer(Server):
    def __handle_event(self, event) -> bool:
        handled = super().__handle_event(event)
        if (handled):
            return True

        match event:
            case _:
                print("Unhandled event for server (CMD)")
                return False
        return True

class CMDServerBuilder(ServerBuilder):
    def build(self) -> Server:
        msg_handler = CMDMessageHandler()
        conn_handler = CMDConnectionHandler()
        key_handler = KeyExchangeHandler()
        return Server(msg_handler, conn_handler, key_handler)

class CMDServerDriver:
    def start():
        print("Starting")
        server = CMDServerBuilder().build()
        server.start()

class CMDConnectionHandler(ConnectionHandler):

    def handle_message_handler_event(self, event: Event) -> bool:
        if isinstance(event, BroadcastAllEvent):
            id = event.get_id()
            text = event.get_text()
            msg = TextMessage(text)
            print("Sending to client")
            for conn in self._connections:
                if not conn.is_id(id):
                    self._connections[conn].send_to_client(msg)
            return True
        else:
            return False

if __name__ == "__main__":
    CMDServerDriver.start()