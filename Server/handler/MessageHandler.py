from Server.events.EncryptedMessageEvent import EncryptedMessageEvent
from common.events.PingEvents import PingEvent
from messages.common.KeyExchangeMessage import KeyExchangeResponseMessage
from messages.common.MessageBuilder import MessageBuilder
from Server.connections.ClientConnectionHandler import ClientMessageEvent, ConnectionID
from common.logging.Logger import Logger
from common.events.EventBus import EventBus
from common.events.Events import Event, EventWithId, EventHandler
from messages.common.Messages import EncryptedMessage
from messages.common.PingMessages import PingMessage
from messages.common.Serializable import Serializable
from messages.common.TextMessage import TextMessage

class MessageHandler(EventHandler, Logger):
    def __init__(self, event_bus: EventBus):
        self.__builder = self._create_message_builder()
        self.event_bus = event_bus
        self.event_bus.subscribe(self)

    def _create_message_builder(self) -> MessageBuilder:
        self.logWarning("WARN: Using default builder")
        return MessageBuilder()

    def on_change(self, event: Event) -> None:
        match event:
            case ClientMessageEvent():
                self.handle_raw_data(event.get_data(), event.get_id())
            case _ :
                pass

    def handle_raw_data(self, raw_data, id: ConnectionID) -> None:
        self.logDebug("Raw data", raw_data)
        msg = self.__builder.rebuild_message(raw_data)
        self.logInfo("Msg", msg.__class__.__name__)
        self.handle_msg(msg, id)
    
    def handle_msg(self, msg: Serializable, id: ConnectionID) -> bool: 
        match msg:
            case KeyExchangeResponseMessage():
                other_y = msg.get_Y()               
                self.event_bus.publish(KeyExchangeResponseEvent(other_y, id))
            case EncryptedMessage():
                self.event_bus.publish(EncryptedMessageEvent(msg, id))
            case PingMessage():
                self.event_bus.publish(PingEvent(msg.get_request_id(), id))
            case TextMessage():
                self.logInfo("Encrypted Text Message", msg.get_msg())
            case _ :
                self.logInfo("Unhandled client message", msg.__class__.__name__) 
                return False
        return True

    def get_builder(self) -> MessageBuilder:
        return self.__builder 

class KeyExchangeResponseEvent(EventWithId):

    def __init__(self, Y: int, id: ConnectionID):
        self.__Y = Y
        self.__id = id

    def get_id(self):
        return self.__id

    def get_y(self) -> int:
        return self.__Y