from RSA.RSAKeyPairGen import RSAKeyPairGen
from RSA.RSAPrivate import RSAPrivateHandler, RSAPrivateKeyReader
from common.events.ConnectionId import ConnectionID
from Server.handler.MessageHandler import KeyExchangeResponseEvent
from common.events.Events import Event, EventWithId, EventDesitination, EventHandler, EventOrigin, EventPublisher
from messages.common.KeyExchangeMessage import KeyExchangeData
from messages.keyExchange.KeyExchanges import KeyExchangeSupport

class ServerKeyExchangeHandler(EventPublisher, KeyExchangeSupport):
    def __init__(self):
        EventPublisher.__init__(self)
        KeyExchangeSupport.__init__(self)

    def __private_key(self) -> RSAPrivateHandler:
        reader = RSAPrivateKeyReader(RSAKeyPairGen.PRIVATE_PATH)
        private_key = reader.handler() 
        return private_key
    
    def signed_Y(self) -> bytes:
        pk = self.__private_key()
        return pk.sign_message(self.Y_bytes())

    def get_data(self):
        return KeyExchangeData(self.Y(), self.signed_Y(), self._base, self._prime)
    

class KeyExchangeHandler(EventHandler, EventPublisher):
    def __init__(self):
        self.connections: dict[ConnectionID, ServerKeyExchangeHandler] = {}
        super().__init__()

    def initiate_new_connection(self, id: ConnectionID):
        handler = self.__new_client()
        handler.register(self)
        handler.set_up(5, 6)
        handler.set_up_this_y(9)
        self.__start_key_exchange(handler.get_data(), id)
        self.connections[id] = handler

    def handle_event(self, event: Event):
        match event:
            case KeyExchangeResponseEvent():
                id = event.get_id()
                self.connections[id].set_up_other_y(event.get_y())
                print("Set up connection")
            case _:
                print("Unexpected message for key handler")

    def K(self, id: ConnectionID) -> int:
        return self.connections[id].K()

    def on_change(self, event: Event):
        self.publish(event)

    def __new_client(self):
        return ServerKeyExchangeHandler() 

    def __start_key_exchange(self, data: KeyExchangeData, id: ConnectionID):
        self.publish(KeyExchangeStartEvent(data, id))

class KeyExchangeStartEvent(EventWithId):
    def __init__(self, msg: KeyExchangeData, id: ConnectionID):
        self.__msg = msg
        self.__id = id

    def get_id(self):
        return self.__id

    def get_data(self) -> KeyExchangeData:
        return self.__msg

    def get_destination(self):
        return EventDesitination.COMMUNICATION_HANDLER
    
    def get_origin(self):
        return EventOrigin.KEY_EXCHANGE_HANDLER
