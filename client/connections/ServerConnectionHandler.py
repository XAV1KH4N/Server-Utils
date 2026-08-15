import threading
import socket
from messages.common.TextMessage import TextMessage
from common.events.Events import EventPublisher
from common.ConnectionUtils import ConnectionUtils
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder
from messages.common.Serializable import Serializable
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

class ClientSideKeyExchangeHandler(KeyExchangeSupport):
    def __init__(self, y: int):
        self.is_enabled = False
        self.set_up_this_y(y)

    def init_from_msg(self, msg: KeyExchangeInitMessage):
        signature = msg.get_signature()
        Y = msg.get_Y()
        self.verify_signature(Y, signature)

        self.set_up_other_y(msg.get_Y())
        self.set_up(msg.get_base(), msg.get_prime())
        print("Setted Up", self.K())

    def verify_signature(self, Y: int, signature: bytes):
        key_handler = self.__load_public_key_handler()
        y_bytes = EncryptUtils.to_bytes(Y)
        key_handler.verify_message(y_bytes, signature)
        print("Verified")

    def __load_public_key_handler(self):
        reader = RSAPublicKeyReader(RSAKeyPairGen.PUBLIC_PATH)
        return reader.handler()

class ServerConnectionHandler(EventPublisher):
    def __init__(self):
        self.__socket = None
        self.__running = False
        self.__message_builder = MessageBuilder()
        self.__key_handler = ClientSideKeyExchangeHandler(91)
        super().__init__()

    def is_running(self) -> bool: 
        return self.__running

    def with_connection(self, main_loop) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ConnectionUtils.HOST, ConnectionUtils.PORT))
                self.__socket = s
                self.__run_in_background()
                main_loop()

        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server")
        except KeyboardInterrupt:
            print("\nForce quitting...")

    def __run_in_background(self):
        self.__running = True
                
        listener_thread = threading.Thread(target=self.__listen)
        listener_thread.daemon = True
        listener_thread.start()

    def __handle_msg_map(self, data: bytes) -> None:
        #inner_msg = self.__message_builder.extract_message(msg)
        msg = self.__message_builder.rebuild_message(data)
        print("Handling Msg Map", msg)
        #inner_msg = self.__message_builder.extract_message(msg)
        self.__handle_msg(msg)

    def __handle_msg(self, msg: Serializable) -> None:
        match msg:
            case KeyExchangeInitMessage():
                print("Key Innit Msg")
                self.__key_handler.init_from_msg(msg)
                msg = KeyExchangeResponseMessage(self.__key_handler.Y())
                self.send_to_server(msg)
                self.send_to_server_encrypted(TextMessage("Hello"))
                print("Send encrypted")
            case EncryptedMessage():
                dec_msg = self.encryptor().recreate_message(msg)
                self.__handle_msg(dec_msg)
            case TextMessage():
                print("Recived encryted: ", msg.get_msg())
            case _:
                print("Unhandled msg")

    def encryptor(self) -> EncryptMessageBuilder:
        return EncryptMessageBuilder(self.__key_handler.K(), self.__message_builder)

    def send_to_server(self, msg: Serializable) -> None:
        final_msg = self.__message_builder.build_message_bytes(msg)
        self.__socket.sendall(final_msg)

    def send_to_server_encrypted(self, msg: Serializable) -> None:
        final_msg = self.__message_builder.build_encrypted_message_bytes(msg, self.encryptor())
        self.__socket.sendall(final_msg)

    def __listen(self):
        print("Listening")
        try:
            while self.__running:
                data = self.__socket.recv(ConnectionUtils.RECV_SIZE)
                if not data:
                    print("Disconected via server")
                    self.__running = False
                else:
                    print("Recieved ", data.__class__.__name__)
                    self.__handle_msg_map(data)

        except KeyboardInterrupt as ex:
            print(f"[ERROR] {ex}")
            self._terminate()