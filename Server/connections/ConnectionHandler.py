from Server.connections.ClientConnectionHandler import ClientConnectionHandler 
from common.logging.Logger import log
from common.events.Events import Event, EventOrigin, EventPublisher, EventHandler, EventDesitination
from messages.keyExchange.KeyExchanges import KeyExchangeStartEvent

class ConnectionHandler(EventHandler, EventPublisher): # Does not need to be extended
    def __init__(self):
        self.__connections: list[ClientConnectionHandler] = [] 
        super().__init__()
        
    def new_connection(self, conn, addr):
        log("New Connection", addr)
        handler = ClientConnectionHandler(conn, addr)
        handler.register(self)
        self.__connections.append(handler) 
        handler.run_in_background()
        handler.start_key_exchange()

    def handle_event(self, event: Event):
        match event.get_origin:
            case EventOrigin.KEY_EXCHANGE_HANDLER:
                self.__handle_key_exchange_event(event)
            case _:
                log("Unexpected event", event)
            
    def __handle_key_exchange_event(self, event: Event):
        match event:
            case KeyExchangeStartEvent():
                msg = event.get_msg()
                # Need an id system
                self.__connections(0).send_to_server(msg)
            case _ :
                log("Unexpecte event from key exchange handler") 
    

    def on_change(self, event: Event):
        match event.get_destination():
            case EventDesitination.COMMUNICATION_HANDLER:
                pass
            case _:
                self.publish(event)