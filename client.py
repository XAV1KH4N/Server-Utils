import socket
import config as cg

class Driver:
    def __init__(self):
        self.start()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((cg.Config.HOST, cg.Config.PORT))
            #recieved_msg = s.recv(len(MESSAGE))
            #print(recieved_msg.decode())
            client = Client(s)
            client.mainLoop()
            s.close()

class Client:
    def __init__(self, socket):
        self.socket = socket

    def mainLoop(self):
        run = True
        while run:
            self.mainPage()
            i = input(": ")
            if (i == "1"):
                run = self.handleSend()
            elif (i == "2"):
                run = self.handleExit() 

    def mainPage(self):
        print("""
            ### Client ###
            (1) Send Message
            (2) Exit  
            """)
        
    def handleSend(self):
        print("""
              Send Message
              """)
        i = input(": ")
        self.socket.sendall(i.encode())
        return True

        
    def handleExit(self):
        return False
        
if (__name__ == "__main__"):
    Driver()
