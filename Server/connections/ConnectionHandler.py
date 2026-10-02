from Server.connections.ClientConnectionHandler import ClientConnectionHandler, ConnectionID 
from Server.handler.KeyExchangeHandler import KeyExchangeStartEvent
from common.logging.Logger import Logger
from common.events.EventBus import EventBus
from common.events.Events import Event, EventHandler
from messages.common.KeyExchangeMessage import KeyExchangeInitMessage
from messages.common.MessageBuilder import MessageBuilder

class ConnectionHandler(Logger):
    def __init__(self, event_bus: EventBus):
        self._connections: dict[ConnectionID, ClientConnectionHandler] = {}
        self.event_bus = event_bus
        self.event_bus.subscribe(self)
        
    def new_connection(self, conn, addr, msg_builder: MessageBuilder) -> ConnectionID:
        self.logInfo("New Connection", addr)
        handler = ClientConnectionHandler(conn, addr, msg_builder, self.event_bus)
        id = handler.get_connection_id()
        self._connections[id] = handler 
        handler.run_in_background()
        return id

    def on_change(self, event: Event):
        match event:
            case KeyExchangeStartEvent():
                key_data = event.get_data()
                id = event.get_id()
                msg = KeyExchangeInitMessage(key_data)
                self._connections[id].send_to_client(msg)
            case _:
                pass