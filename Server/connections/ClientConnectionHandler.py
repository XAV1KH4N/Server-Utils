import threading
from common.RequestWorker import RequestWorker
from common.events.ConnectionId import ConnectionID
from common.events.EventBus import EventBus
from common.events.Events import Event, EventHandler, EventWithId, EventWithRequest
from common.logging.Logger import Logger
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Serializable import Requestable, Serializable


class ClientConnectionHandler(Logger, EventHandler): 
    def __init__(self, conn, addr, msg_builder: MessageBuilder, event_bus: EventBus):
        self.__conn = conn
        self.__id = ConnectionID(addr)
        self.__is_running = True
        self.__message_builder = msg_builder
        self.__event_bus = event_bus
        event_bus.subscribe(self)
        self.__watching: list[RequestWorker] = []

    def on_change(self, event: Event) -> None:
        for worker in self.__watching:
            if (isinstance(event, EventWithRequest)):
                event.get_request_id() == worker.get_request()
                if (isinstance(event, worker.response_event_type())):
                    worker.on_complete(event)
                    self.__watching.remove(worker)
                    return

    def get_connection_id(self) -> ConnectionID:
        return self.__id

    def send_to_client(self, msg: Serializable):
        data = self.__message_builder.build_message_bytes(msg)
        self.__conn.sendall(data)
        self.logInfo("Sent", msg.__class__.__name__)

    def request_to_client(self, worker: RequestWorker):
        data = self.__message_builder.build_message_bytes(worker.get_request())
        self.__conn.sendall(data)
        self.__watching.append(worker)
        self.logInfo("Requested", worker.get_request().__class__.__name__)

    def run_in_background(self):
        listener = threading.Thread(target=self.__listen_loop)
        listener.daemon = True
        listener.start()

    def __listen_loop(self):
        self.logInfo("Listening")
        with self.__conn:
            try:
                while self.__is_running:
                    data = self.__conn.recv(1024)
                    self.logInfo("data ", data)
                    if not data:
                        self.logWarning("Connection terminated by peer")
                        self.__is_running = False
                    else:
                        self.__event_bus.publish(ClientMessageEvent(data, self.__id))
            except KeyboardInterrupt:
                self.logError(f"\nConnection error with {self._getAddr()}:")
            finally:
                self._running = False
        self.logInfo("Terminating")
        

class ClientMessageEvent(EventWithId):
    def __init__(self, data, id: ConnectionID):
        self.__data  = data
        self.__id = id

    def get_data(self):
        return self.__data
    
    def get_id(self) -> ConnectionID:
        return self.__id