from abc import ABC
import socket 

from common.events.EventBus import EventBus
from common.events.ConnectionId import ConnectionID
from Server.connections.ConnectionHandler import ConnectionHandler
from Server.events.EncryptedMessageEvent import EncryptedMessageEvent
from Server.handler.KeyExchangeHandler import KeyExchangeHandler
from common.ConnectionUtils import ConnectionUtils
from common.logging.Logger import Logger, log
from common.events.Events import Event, EventHandler
from messages.common.Messages import EncryptedMessage
from messages.common.Serializable import Serializable
from Server.handler.MessageHandler import MessageHandler
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder

class Server(EventHandler, Logger): # Do all at once
    def __init__(self, msg_handler: MessageHandler, conn_handler: ConnectionHandler, key_handler: KeyExchangeHandler, event_bus: EventBus):
        self.__message_handler = msg_handler
        self._connection_handler = conn_handler
        self.__key_exchange_manager = key_handler
        self.__event_bus = event_bus
        self.__event_bus.subscribe(self)

    def start(self):
        self.__listen_loop()

    def on_change(self, event: Event):
        match event:
            case EncryptedMessageEvent():
                msg = event.get_msg()
                id = event.get_id()
                dec_msg = self.__decrypt__message(msg, id)
                self.__message_handler.handle_msg(dec_msg, id)
            case _:
                pass

    def __encryptor_for(self, id: ConnectionID) -> EncryptMessageBuilder:
        k = self.__key_exchange_manager.K(id)
        enc_builder = EncryptMessageBuilder(k, self.__message_handler.get_builder())
        return enc_builder
    
    def __decrypt__message(self, msg: EncryptedMessage, id: ConnectionID) -> Serializable:
        enc_builder = self.__encryptor_for(id)
        print("Msg cipher", msg.get_cipher())
        dec_msg = enc_builder.recreate_message(msg)
        return dec_msg
    
    def __listen_loop(self):
        print("Entering Main Loop")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ConnectionUtils.HOST, ConnectionUtils.PORT))
            s.listen()

            log(f'[SERVER STARTED] Listening on {ConnectionUtils.HOST}:{ConnectionUtils.PORT}...')

            while True:
                try:
                    conn, addr = s.accept() 
                    id = self._connection_handler.new_connection(conn, addr, self.__message_handler.get_builder())
                    self.__key_exchange_manager.initiate_new_connection(id)
                except KeyboardInterrupt:
                    log("[SHUTTING DOWN] Server shutting down manually.")
                    break
                #except Exception as e:
                #    log(f"[SERVER ERROR] {e}")
                #    break


class ServerBuilder(ABC):
    def build() -> Server:
        pass

class TestServerBUilder(ServerBuilder):
    def build(self) -> Server:
        msg_handler = MessageHandler()
        conn_handler = ConnectionHandler()
        key_handler = KeyExchangeHandler()
        return Server(msg_handler, conn_handler, key_handler)

class ServerDriver:
    def start():
        print("Starting")
        server = TestServerBUilder().build()
        server.start()

if __name__ == "__main__":
    ServerDriver.start()