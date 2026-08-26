from messages.common.TextMessage import TextMessage
from client.client import Client
from teminal.common.messages.Broadcast import BroadcastMessage

class CMDClient(Client):
    def __init__(self):
        super().__init__()
        self.__running = True

    def main_loop(self):
        while self.__running:
            self.__print_options()
            choice = input("-> ")
            valid, cleaned_choice = self.__validate_input(choice)
            if (valid):
                match cleaned_choice:
                    case 1:
                        self.__send_msg_to_server()
                    case 2:
                        self.__handle_broadcast()
                    case 3:
                        self.__running = False
                    case _:
                        print("Missing implementation")

            else:
                print("Invalid Message")

    def __send_msg_to_server(self):
        msg = input("Enter Message: ")
        msg_data = TextMessage(msg)
        self._connection_handler.send_to_server_encrypted(msg_data)
        print("Encrypted + Sent")        

    def __handle_broadcast(self):
        msg = input("Enter Message: ")
        msg_data = BroadcastMessage(msg)
        self._connection_handler.send_to_server_encrypted(msg_data)
        print("Encrypted + Broadcasted")

    def __validate_input(self, choice: str):
        valid = [1, 2, 3]
        try:
            i = int(choice)      
            return (i in valid), i
        except:
            return False, -1

    def __print_options(self) -> None:
        print('''
        Options ... 
           (1) Send to Server
           (2) Broadcast to clients
           (3) Terminate
        ''')

class ClientDriver:
    def start():
        CMDClient().start()

if __name__ == "__main__":
    ClientDriver.start()