import threading
from common.logging.Logger import log
from common.events.Events import Event, EventOrigin, EventPublisher, EventDesitination
from messages.common.KeyExchangeMessage import KeyExchangeData, KeyExchangeInitMessage
from messages.keyExchange.KeyExchanges import KeyExchangeStartEvent
from messages.common.MessageBuilder import MessageBuilder

class ClientConnectionHandler(EventPublisher):
    def __init__(self, conn, addr):
        self.__conn = conn
        self.__addr = addr
        self.__is_running = True
        self.__message_builder = MessageBuilder()
        super().__init__()

    def run_in_background(self):
        listener = threading.Thread(target=self.__listen_loop)
        listener.daemon = True
        listener.start()

    def start_key_exchange(self):
        key_data = KeyExchangeData(10, b'1234', 9, 13)
        key_event = KeyExchangeStartEvent(key_data)
        self.publish(key_event)

    def send_key_exchange_client(self, key_data: KeyExchangeData):
        msg = KeyExchangeInitMessage(key_data)
        json_data = self.__message_builder.build_message_bytes(msg)
        self.__conn.sendAll(json_data)

    def __listen_loop(self):
        print("Listening")
        with self.__conn:
            try:
                while self.__is_running:
                    data = self.__conn.recv(1024)
                    print("data ", data)
                    if not data:
                        log("Connection terminated by peer")
                        self.__is_running = False
                    else:
                        self.publish(ClientMessageEvent(data))
            except KeyboardInterrupt:
                log(f"\n[ERROR] Connection error with {self._getAddr()}:")
            finally:
                self._running = False

class ClientMessageEvent(Event):
    def __init__(self, data):
        self.__data  = data

    def get_data(self):
        return self.__data
    
    def get_destination(self):
        return EventDesitination.MESSAGE_HANDLER
    
    def get_origin(self):
        return EventOrigin.COMMUNICATION_HANDLER