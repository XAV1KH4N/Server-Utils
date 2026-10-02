from random import Random
from RSA.RSAKeyPairGen import RSAKeyPairGen
from RSA.RSAPrivate import RSAPrivateHandler, RSAPrivateKeyReader
from common.events.ConnectionId import ConnectionID
from Server.handler.MessageHandler import KeyExchangeResponseEvent
from common.events.EventBus import EventBus
from common.events.Events import Event, EventWithId, EventHandler
from messages.common.KeyExchangeMessage import KeyExchangeData
from messages.keyExchange.KeyExchanges import KeyExchangeSupport

class ServerKeyExchangeHandler(KeyExchangeSupport):
    def __init__(self):
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
    

class KeyExchangeHandler(EventHandler):
    def __init__(self, event_bus: EventBus):
        self.connections: dict[ConnectionID, ServerKeyExchangeHandler] = {}
        self.event_bus = event_bus
        self.event_bus.subscribe(self)

    def initiate_new_connection(self, id: ConnectionID):
        handler = self.__new_client()
        base = self.__generate_base()
        prime = self.__generate_prime()
        y = self.__generate_y()
        handler.set_up(base, prime)
        handler.set_up_this_y(y)
        self.__start_key_exchange(handler.get_data(), id)
        self.connections[id] = handler

    def K(self, id: ConnectionID) -> int:
        return self.connections[id].K()

    def on_change(self, event: Event):
        match event:
            case KeyExchangeResponseEvent():
                id = event.get_id()
                self.connections[id].set_up_other_y(event.get_y())
                print("Set up connection")
            case _:
                pass
    
    def __generate_base(self) -> int:
        return Random().randint(0, 1000000) 

    def __generate_y(self) -> int:
        return Random().randint(0, 1000000) 

    def __generate_prime(self) -> int:
        return 13
    
    def __new_client(self):
        return ServerKeyExchangeHandler() 

    def __start_key_exchange(self, data: KeyExchangeData, id: ConnectionID):
        self.event_bus.publish(KeyExchangeStartEvent(data, id))

class KeyExchangeStartEvent(EventWithId):
    def __init__(self, msg: KeyExchangeData, id: ConnectionID):
        self.__msg = msg
        self.__id = id

    def get_id(self):
        return self.__id

    def get_data(self) -> KeyExchangeData:
        return self.__msg