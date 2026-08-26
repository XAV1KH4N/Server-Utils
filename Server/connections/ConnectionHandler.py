from Server.connections.ClientConnectionHandler import ClientConnectionHandler, ConnectionID 
from Server.handler.KeyExchangeHandler import KeyExchangeStartEvent
from common.logging.Logger import log
from common.events.Events import Event, EventOrigin, EventPublisher, EventHandler, EventDesitination
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage
from messages.common.MessageBuilder import MessageBuilder

class ConnectionHandler(EventHandler, EventPublisher):
    def __init__(self):
        self._connections: dict[ConnectionID, ClientConnectionHandler] = {}
        super().__init__()
        
    def new_connection(self, conn, addr, msg_builder: MessageBuilder) -> ConnectionID:
        log("New Connection", addr)
        handler = ClientConnectionHandler(conn, addr, msg_builder)
        id = handler.get_connection_id()
        handler.register(self)
        self._connections[id] = handler 
        handler.run_in_background()
        return id

    def handle_event(self, event: Event) -> bool:
        print("Connection Handler", event)
        match event.get_origin():
            case EventOrigin.KEY_EXCHANGE_HANDLER: 
                self.handle_key_exchange_event(event)
            case EventOrigin.MESSAGE_HANDLER:
                self.handle_message_handler_event(event)
            case _:
                log("Unexpected event", event, event.get_origin())
                return False

        return True

    def handle_message_handler_event(self, event: Event) -> bool:
        print("unhandled event")
        return False

    def handle_key_exchange_event(self, event: Event):
        if isinstance(event, KeyExchangeStartEvent):
            key_data = event.get_data()
            id = event.get_id()
            msg = KeyExchangeInitMessage(key_data)
            self._connections[id].send_to_client(msg)

    def on_change(self, event: Event):
        match event.get_destination():
            case EventDesitination.COMMUNICATION_HANDLER:
                self.handle_event(event)
            case _:
                self.publish(event)