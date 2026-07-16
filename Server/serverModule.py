# Forget abstracting
# Server will always need to first, verify connection
# Verify the user
# Then we can then go into the what the rest of apps want to do
# So maybe subclassing


# For each connection
# - Message Handling (Own encryoted messages)
# - - But once decrypted, can be sent to message handling for all users


# Message Handler (Singleton)
# - Takes a message + the current user (just added meta data)
# - Then handles it, and then finds the communication for that user and sends once done
# - - This is async. Maybe make some sort of worker. Sends reqyest and waits on a thread
# - Can take support for additional messages and there mappings

# Connection Handler (Singleton)
# Manged a list of connections
# can find a connection based on meta data like username
# Single thread to listent
# - Handles new connection, not the main server

# DB Handler (Singleton)
# Manages login stuff
# Extends to manage extra

# Encrytion Builder (Per Connection)
# - K will be different for each connection

# ServerModule
# - Message Handler (To Be Extended)
# - Connection Handler

# Lets say i want...
# A message to send a message to another user
# Message will be handled by Message handler
# Which i extend, and handled there
# Now need to speak to DB
# Ive extended DB handler
# How to get the two to speak? Raise an event from one
# Event includes, who the message is for (I.e DBModule)
# Plus the request
# Server listens to handler, then forwards the message (maybe its put on a queue, handled by another thread)
# Handler recieves, then forwards a response back if needed
# Some util worker that will wait for a response 

from Server.connections.ConnectionHandler import ConnectionHandler
from common.ConnectionUtils import ConnectionUtils
from common.logging.Logger import log
from common.events.Events import Event, EventHandler, EventDesitination
import socket 
from Server.handler.MessageHandler import MessageHandler

class Server(EventHandler):
    def __init__(self):
        self.__message_handler = MessageHandler()
        self.__connection_handler = ConnectionHandler()

    def start(self):
        self.__addListeners()
        self.__listen_loop()

    def on_change(self, event: Event):
        match event.getDestination():
            case EventDesitination.MESSAGE_HANDLER:
                self.__message_handler.handle_event(event)
            case _ : 
                log("Even has unknown location")

    def __addListeners(self):
        self.__connection_handler.register(self)
        self.__message_handler.register(self)

    def __listen_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ConnectionUtils.HOST, ConnectionUtils.PORT))
            s.listen()

            log(f'[SERVER STARTED] Listening on {ConnectionUtils.HOST}:{ConnectionUtils.PORT}...')

            while True:
                try:
                    conn, addr = s.accept() 
                    self.__connection_handler.new_connection(conn, addr)
                except KeyboardInterrupt:
                    log("[SHUTTING DOWN] Server shutting down manually.")
                    break
                except Exception as e:
                    log(f"[SERVER ERROR] {e}")
                    break

class ServerDriver:
    def start():
        Server().start()

if __name__ == "__main":
    ServerDriver.start()