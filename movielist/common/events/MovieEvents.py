from common.events.ConnectionId import ConnectionID
from common.events.Events import Event, EventWithId, EventWithRequest
from movielist.common.Movie import MovieEntry

class GetMovieRequestEvent(EventWithId, EventWithRequest):
    def __init__(self, request_id: str, connection_id: ConnectionID):
        self.__request_id = request_id
        self.__connection_id = connection_id

    def get_id(self) -> ConnectionID:
        return self.__connection_id

    def get_request_id(self) -> str:
        return self.__request_id

class GetMovieResponseEvent(EventWithRequest):
    def __init__(self, request_id: str, entries: list[MovieEntry]):
        self.__request_id = request_id
        self.entries = entries

    def get_request_id(self) -> str:
        return self.__request_id

    def get_entries(self) -> list[MovieEntry]:
        return self.entries

class AddMovieEvent(Event):
    def __init__(self, entry: MovieEntry):
        self.__entry = entry

    def get_entry(self):
        return self.__entry

class DeleteMovieEvent(Event):
    def __init__(self, entry: MovieEntry):
        self.__entry = entry

    def get_entry(self):
        return self.__entry