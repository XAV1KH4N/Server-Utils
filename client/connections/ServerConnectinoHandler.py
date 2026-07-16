import threading
import socket
from common.events.Events import Event, EventOrigin, EventPublisher, EventDesitination
from common.EncyptUtils import EncryptUtils
class ServerConnectionHandler(EventPublisher):
    def __init__(self):
        self.__socket = None
        self.__running = False

    def __initiate_connection(self) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((EncryptUtils.HOST, EncryptUtils.PORT))
                self.__socket = s
                
        except ConnectionRefusedError:
            print("[ERROR] Could not connect to server")
        except KeyboardInterrupt:
            print("\nForce quitting...")

    def run_in_background(self):
        self.__running = self.__initiate_connection()
                
        listener_thread = threading.Thread(target=self.__listen)
        listener_thread.daemon = True
        listener_thread.start()

    def __listen(self):
        while self.__running:
            pass


class ServerMessageEvent(Event):

