from common.logging.Logger import log
from common.events.Events import Event, EventPublisher, EventHandler, EventDesitination
from Server.connections.ClientConnectionHandler import ClientConnectionHandler

class ConnectionHandler(EventHandler, EventPublisher): # Does not need to be extended
    def __init__(self):
        self.__connections: list[ClientConnectionHandler] = [] 

    def new_connection(self, conn, addr):
        handler = ClientConnectionHandler(conn, addr)
        handler.register(self)
        self.__connections.append(handler) 
        handler.run()

    def on_change(self, event: Event):
        match event.getDestination():
            case EventDesitination.COMMUNICATION_HANDLER:
                pass
            case _:
                self.publish(event)