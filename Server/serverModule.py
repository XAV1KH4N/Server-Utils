import socket 

from common.events.ConnectionId import ConnectionID
from Server.connections.ConnectionHandler import ConnectionHandler
from Server.events.EncryptedMessageEvent import EncryptedMessageEvent
from Server.handler.KeyExchangeHandler import KeyExchangeHandler
from common.ConnectionUtils import ConnectionUtils
from common.logging.Logger import log
from common.events.Events import Event, EventHandler, EventDesitination
from messages.common.Messages import EncryptedMessage
from messages.common.Serializable import Serializable
from Server.handler.MessageHandler import MessageHandler
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder
from messages.common.MessageBuilder import MessageBuilder

# Sub Server
# Extends server?
# Will have to for passing messages.. Or will it? It has origin/desitnations - so no
# Message Handler will need to be extends.
# start with client, main loop
class Server(EventHandler):
    def __init__(self):
        self.__message_handler = MessageHandler()
        self.__connection_handler = ConnectionHandler()
        self.__key_exchange_manager = KeyExchangeHandler()

    def start(self):
        self.__add_listeners()
        self.__listen_loop()

    def on_change(self, event: Event):
        match event.get_destination():
            case EventDesitination.MESSAGE_HANDLER:
                self.__message_handler.handle_event(event)
            case EventDesitination.COMMUNICATION_HANDLER:
                self.__connection_handler.handle_event(event)
            case EventDesitination.KEY_EXCHANGE_HANDLER:
                self.__key_exchange_manager.handle_event(event)
            case EventDesitination.SERVER:
                self.__handle_event(event)
            case _ : 
                log("Event has unknown location", event.get_destination())

    def __handle_event(self, event: Event):
        print("Handling event", event.__class__.__name__)
        match event:
            case EncryptedMessageEvent():
                msg = event.get_msg()
                id = event.get_id()
                dec_msg = self.__decrypt__message(msg, id)
                self.__message_handler.handle_msg(dec_msg, id)
            case _:
                print("Unhandled event for server")

    def __encryptor_for(self, id: ConnectionID) -> EncryptMessageBuilder:
        k = self.__key_exchange_manager.K(id)
        builder = MessageBuilder()
        enc_builder = EncryptMessageBuilder(k, builder)
        return enc_builder
    
    def __decrypt__message(self, msg: EncryptedMessage, id: ConnectionID) -> Serializable:
        enc_builder = self.__encryptor_for(id)
        print("Msg cipher", msg.get_cipher())
        dec_msg = enc_builder.recreate_message(msg)
        return dec_msg
    
    def __add_listeners(self):
        self.__connection_handler.register(self)
        self.__message_handler.register(self)
        self.__key_exchange_manager.register(self)

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
                    id = self.__connection_handler.new_connection(conn, addr)
                    self.__key_exchange_manager.initiate_new_connection(id)
                except KeyboardInterrupt:
                    log("[SHUTTING DOWN] Server shutting down manually.")
                    break
                #except Exception as e:
                #    log(f"[SERVER ERROR] {e}")
                #    break

class ServerDriver:
    def start():
        print("Starting")
        Server().start()

if __name__ == "__main__":
    ServerDriver.start()