import threading
import socket
from common.RequestWorker import RequestWorker
from common.events.PingEvents import PongEvent
from common.events.EventBus import EventBus
from common.events.Events import Event, EventHandler, EventWithRequest
from common.logging.Logger import Logger
from messages.common.PingMessages import PingMessage, PongMessage
from messages.common.TextMessage import TextMessage
from common.ConnectionUtils import ConnectionUtils
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder
from messages.common.Serializable import Requestable, Serializable
from messages.common.MessageBuilder import MessageBuilder
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage, KeyExchangeResponseMessage
from messages.common.Messages import EncryptedMessage
from RSA.RSAPublic import RSAPublicKeyReader
from RSA.RSAKeyPairGen import RSAKeyPairGen
from common.EncyptUtils import EncryptUtils
from messages.keyExchange.KeyExchanges import KeyExchangeSupport

class EncryptionHandler:
    def __init__(self):
        pass

class ClientSideKeyExchangeHandler(KeyExchangeSupport, Logger):
    def __init__(self, y: int):
        self.is_enabled = False
        self.set_up_this_y(y)

    def init_from_msg(self, msg: KeyExchangeInitMessage):
        signature = msg.get_signature()
        Y = msg.get_Y()
        self.verify_signature(Y, signature)

        self.set_up_other_y(msg.get_Y())
        self.set_up(msg.get_base(), msg.get_prime())
        self.logDebug("Setted Up", self.K())

    def verify_signature(self, Y: int, signature: bytes):
        key_handler = self.__load_public_key_handler()
        y_bytes = EncryptUtils.to_bytes(Y)
        key_handler.verify_message(y_bytes, signature)
        self.logInfo("Verified")

    def __load_public_key_handler(self):
        reader = RSAPublicKeyReader(RSAKeyPairGen.PUBLIC_PATH)
        return reader.handler()

class ServerConnectionHandler(Logger, EventHandler):
    def __init__(self, event_bus: EventBus, message_builder ):
        self.__socket = None
        self.__running = False
        self.__is_verified = False
        self._pinged = False
        self.__message_builder = message_builder
        self.__key_handler = ClientSideKeyExchangeHandler(91)
        self._event_bus = event_bus
        event_bus.subscribe(self)   
        self.__watching: list[RequestWorker] = []

    def on_change(self, event: Event) -> None:
        for worker in self.__watching:
            self.logDebug("Comapre", event, isinstance(event, EventWithRequest))
            if (isinstance(event, EventWithRequest)):
                event.get_request_id() == worker.get_request()
                if (isinstance(event, worker.response_event_type())):
                    worker.on_complete(event)
                    self.__watching.remove(worker)
                    return

    def is_running(self) -> bool: 
        return self.__running

    def with_connection(self, main_loop) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ConnectionUtils.HOST, ConnectionUtils.PORT))
                self.__socket = s
                self.__run_in_background()

                self.logDebug("Waiting on verification")
                while not self.__is_verified:
                    pass

                self.logDebug("Waiting on pong")
                while not self._pinged:
                    pass

                self.logInfo("Verified, Starting main loop")
                main_loop()

        except ConnectionRefusedError:
            self.logError("Could not connect to server")
        except KeyboardInterrupt:
            self.logInfo("\nForce quitting...")

    def __run_in_background(self):
        self.__running = True
                
        listener_thread = threading.Thread(target=self.__listen)
        listener_thread.daemon = True
        listener_thread.start()

    def __handle_msg_map(self, data: bytes) -> None:
        msg = self.__message_builder.rebuild_message(data)
        self.logInfo("Handling Msg Map", msg)
        self._handle_msg(msg)

    def _handle_msg(self, msg: Serializable) -> None:
        match msg:
            case KeyExchangeInitMessage():
                self.logDebug("Key Innit Msg")
                self.__key_handler.init_from_msg(msg)
                self.__is_verified = True
                msg = KeyExchangeResponseMessage(self.__key_handler.Y())
                self.send_to_server(msg)
                self.__ping()
            case EncryptedMessage():
                dec_msg = self.encryptor().recreate_message(msg)
                self._handle_msg(dec_msg)
            case PongMessage():
                self._event_bus.publish(PongEvent(msg.get_request_id()))     
            case TextMessage():
                self.logDebug("Recived encryted: ", msg.get_msg())
            case _:
                self.logInfo("Unhandled msg")

    def encryptor(self) -> EncryptMessageBuilder:
        return EncryptMessageBuilder(self.__key_handler.K(), self.__message_builder)

    def request_to_worker(self, worker: RequestWorker) -> None:
        msg = worker.get_request()
        if (self.__is_verified):
            self.logInfo("Sending encrypted request")
            final_msg = self.__message_builder.build_encrypted_message_bytes(msg, self.encryptor())
        else:
            final_msg = self.__message_builder.build_message_bytes(msg)
            self.logWarning("Sending unencrypted request")

        self.__watching.append(worker)
        self.__socket.sendall(final_msg)

    def send_to_server(self, msg: Serializable) -> None:
        final_msg = self.__message_builder.build_message_bytes(msg)
        self.__socket.sendall(final_msg)

    def send_to_server_encrypted(self, msg: Serializable) -> None:
        final_msg = self.__message_builder.build_encrypted_message_bytes(msg, self.encryptor())
        self.__socket.sendall(final_msg)

    def __listen(self):
        self.logInfo("Listening")
        try:
            while self.__running:
                data = self.__socket.recv(ConnectionUtils.RECV_SIZE)
                if not data:
                    self.logWarning("Disconected via server")
                    self.__running = False
                else:
                    self.logInfo("Recieved ", data.__class__.__name__)
                    self.__handle_msg_map(data)

        except KeyboardInterrupt as ex:
            self.logError(f"{ex}")
            self._terminate()

    
    def __ping(self) -> None:

        class PingWorker(RequestWorker):
            def get_request(self) -> Requestable:
                return PingMessage()

            def response_event_type(self): 
                return PongEvent

            def on_complete(inner_self, result: PongEvent) -> None:
                self.logInfo("Recieved Pong")
                print(self._pinged)
                self._pinged = True
                print(self._pinged)

            def on_failure(inner_self) -> None:
                self.logError("Failed to recieve Pong")

        self.logInfo("Sending Ping")
        self.request_to_worker(PingWorker())