from messages.common.MessageBuilder import MessageBuilder
from Server.connections.ConnectionHandler import ConnectionHandler
from Server.connections.ClientConnectionHandler import ClientMessageEvent
from common.logging.Logger import log
from common.events.Events import Event, EventOrigin, EventHandler, EventDesitination, EventPublisher
from messages.common.MessageBuilder import MessageBuilder

class MessageHandler(EventPublisher):
    def __init__(self):
        self.__builder = MessageBuilder()

    def handle_event(self, event: Event) -> None:
        match event.getOrigin:
            case EventOrigin.COMMUNICATION_HANDLER:
                self.handle_communication_event(event)
            case _ : 
                 log("Unhanlded client message")

    def handle_communication_event(self, event: Event) -> None:
        match event:
            case ClientMessageEvent(data = raw_data):
                self.handle_raw_data(raw_data)
            case _ :
                log("Unhandled client message")

    def handle_raw_data(self, raw_data) -> None:
        msg = self.__builder.rebuild_message(raw_data)
        match msg:
            case _: 
                log("Unhandled client message")
