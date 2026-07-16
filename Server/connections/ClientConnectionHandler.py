import threading
from common.logging.Logger import log
from common.events.Events import Event, EventOrigin, EventPublisher, EventDesitination

class ClientConnectionHandler(EventPublisher):
    def __init__(self, conn, addr):
        self.__conn = conn
        self.__addr = addr
        self.__is_running = True

    def run(self):
        listener = threading.Thread(target=self.__listen_loop)
        listener.daemon = True
        listener.start()

    def __listen_loop(self):
        with self.__conn:
            try:
                while self.__is_running:
                    data = self._conn.recv(1024)
                    if not data:
                        log("Conenction terminated by peer")
                        self.__is_running = False
                    else:
                        self.publish(ClientMessageEvent(data))
            except:
                log(f"\n[ERROR] Connection error with {self._getAddr()}:")
            finally:
                self._running = False

class ClientMessageEvent(Event):
    def __init__(self, data):
        self.__data  = data

    def getData(self):
        return self.__data
    
    def getDestination(self):
        return EventDesitination.MESSAGE_HANDLER
    
    def getOrigin(self):
        return EventOrigin.COMMUNICATION_HANDLER