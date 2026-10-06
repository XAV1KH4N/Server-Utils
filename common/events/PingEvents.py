from common.events import ConnectionId
from common.events.Events import EventWithId, EventWithRequest

class PingEvent(EventWithRequest, EventWithId):

    def __init__(self, request_id, connection_id):
        self.__request_id = request_id
        self.__connection_id = connection_id

    def get_request_id(self) -> str:
        return self.__request_id

    def get_id(self) -> ConnectionId:
        return self.__connection_id

class PongEvent(EventWithRequest):

    def __init__(self, request_id):
        self.__request_id = request_id

    def get_request_id(self) -> str:
        return self.__request_id

