from Server.connections.ConnectionHandler import ConnectionHandler
from Server.handler.KeyExchangeHandler import KeyExchangeHandler
from common.ConnectionUtils import ConnectionUtils
from common.logging.Logger import log
from common.events.Events import Event, EventHandler, EventDesitination
import socket 
from Server.handler.MessageHandler import MessageHandler

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
            case _ : 
                log("Even has unknown location")

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
                    self.__connection_handler.new_connection(conn, addr)
                    self.__key_exchange_manager.initiate_new_connection()
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