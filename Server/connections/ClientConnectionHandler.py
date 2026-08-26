from random import Random
import threading
from common.events.ConnectionId import ConnectionID
from common.events.Events import Event, EventOrigin, EventPublisher, EventDesitination, EventWithId
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Serializable import Serializable


class ClientConnectionHandler(EventPublisher): 
    def __init__(self, conn, addr, msg_builder: MessageBuilder):
        self.__conn = conn
        self.__id = ConnectionID(addr)
        self.__is_running = True
        self.__message_builder = msg_builder
        super().__init__()

    def get_connection_id(self) -> ConnectionID:
        return self.__id

    def send_to_client(self, msg: Serializable):
        data = self.__message_builder.build_message_bytes(msg)
        self.__conn.sendall(data)
        print("Sent", msg.__class__.__name__)

    def run_in_background(self):
        listener = threading.Thread(target=self.__listen_loop)
        listener.daemon = True
        listener.start()

    def __listen_loop(self):
        print("Listening")
        with self.__conn:
            try:
                while self.__is_running:
                    data = self.__conn.recv(1024)
                    print("data ", data)
                    if not data:
                        print("Connection terminated by peer")
                        self.__is_running = False
                    else:
                        self.publish(ClientMessageEvent(data, self.__id))
            except KeyboardInterrupt:
                print(f"\n[ERROR] Connection error with {self._getAddr()}:")
            finally:
                self._running = False
        print("Terminating")
        

class ClientMessageEvent(EventWithId):
    def __init__(self, data, id: ConnectionID):
        self.__data  = data
        self.__id = id

    def get_data(self):
        return self.__data
    
    def get_destination(self):
        return EventDesitination.MESSAGE_HANDLER
    
    def get_origin(self):
        return EventOrigin.COMMUNICATION_HANDLER

    def get_id(self) -> ConnectionID:
        return self.__id