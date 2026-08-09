from Server.connections.ClientConnectionHandler import ClientConnectionHandler 
from Server.handler.KeyExchangeHandler import KeyExchangeStartEvent
from common.logging.Logger import log
from common.events.Events import Event, EventOrigin, EventPublisher, EventHandler, EventDesitination
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage

class ConnectionHandler(EventHandler, EventPublisher):
    def __init__(self):
        self.__connections: list[ClientConnectionHandler] = [] 
        super().__init__()
        
    def new_connection(self, conn, addr):
        log("New Connection", addr)
        handler = ClientConnectionHandler(conn, addr)
        handler.register(self)
        self.__connections.append(handler) 
        handler.run_in_background()

    def handle_event(self, event: Event):
        print("Connection Handler", event)
        match event.get_origin():
            case EventOrigin.KEY_EXCHANGE_HANDLER: 
                self.handle_key_exchange_event(event)
            case _:
                log("Unexpected event", event, event.get_origin())

    def handle_key_exchange_event(self, event: Event):
        if isinstance(event, KeyExchangeStartEvent):
            key_data = event.get_data()
            msg = KeyExchangeInitMessage(key_data)
            self.__connections[0].send_to_client(msg)

    def on_change(self, event: Event):
        match event.get_destination():
            case EventDesitination.COMMUNICATION_HANDLER:
                self.handle_event(event)
            case _:
                self.publish(event)