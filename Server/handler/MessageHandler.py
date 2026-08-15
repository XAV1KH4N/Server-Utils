from Server.events.EncryptedMessageEvent import EncryptedMessageEvent
from messages.common.KeyExchangeMessage import KeyExchangeResponseMessage
from messages.common.MessageBuilder import MessageBuilder
from Server.connections.ClientConnectionHandler import ClientMessageEvent, ConnectionID
from common.logging.Logger import log
from common.events.Events import Event, EventDesitination, EventOrigin, EventPublisher, EventWithId
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import EncryptedMessage
from messages.common.Serializable import Serializable
from messages.common.TextMessage import TextMessage

class MessageHandler(EventPublisher):
    def __init__(self):
        self.__builder = MessageBuilder()
        super().__init__()

    def handle_event(self, event: Event) -> None:
        print("Event", event.__class__.__name__)
        print(event.get_origin())
        match event.get_origin():
            case EventOrigin.COMMUNICATION_HANDLER:
                print("Handling", event.__class__.__name__)
                self.handle_communication_event(event)
            case _ : 
                 log("Unhanlded client message")

    def handle_communication_event(self, event: Event) -> None:
        match event:
            case ClientMessageEvent():
                self.handle_raw_data(event.get_data(), event.get_id())
            case _ :
                log("Unhandled client message")

    def handle_raw_data(self, raw_data, id: ConnectionID) -> None:
        print("Raw data", raw_data)
        msg = self.__builder.rebuild_message(raw_data)
        print("Msg", msg.__class__.__name__)
        self.handle_msg(msg, id)
    
    def handle_msg(self, msg: Serializable, id: ConnectionID) -> None: 
        match msg:
            case KeyExchangeResponseMessage():
                other_y = msg.get_Y()               
                self.publish(KeyExchangeResponseEvent(other_y, id))
            case EncryptedMessage():
                self.publish(EncryptedMessageEvent(msg, id))
            case TextMessage():
                print("Encrypted Text Message", msg.get_msg())
            case _ :
                log("Unhandled client message") 

class KeyExchangeResponseEvent(EventWithId):

    def __init__(self, Y: int, id: ConnectionID):
        self.__Y = Y
        self.__id = id

    def get_id(self):
        return self.__id

    def get_y(self) -> int:
        return self.__Y

    def get_destination(self) -> EventDesitination:
        return EventDesitination.KEY_EXCHANGE_HANDLER

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER
