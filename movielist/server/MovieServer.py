from Server.connections.ConnectionHandler import ConnectionHandler
from Server.handler.KeyExchangeHandler import KeyExchangeHandler
from Server.serverModule import ServerBuilder, Server
from common.events.EventBus import EventBus
from common.events.Events import Event
from common.logging.Logger import Logger
from movielist.common.MovieRequests import GetMoviesResponse, GetMoviesResponseData
from movielist.common.events.MovieEvents import AddMovieEvent, DeleteMovieEvent, GetMovieRequestEvent, GetMovieResponseEvent
from movielist.server.MovieCacheManager import MovieCacheManager
from movielist.server.MovieMessageHandler import MovieMessageHandler

class MovieServer(Server):
    def on_change(self, event: Event) -> bool:
        handled = super().on_change(event)
        if (handled):
            return True

        match event:
            case _:
                self.logError("Unhandled event for server (CMD)")
                return False
        return True

class MovieServerBuilder(ServerBuilder):
    def build(self) -> Server:
        event_bus = EventBus()
        msg_handler = MovieMessageHandler(event_bus)
        conn_handler = MovieConnectionHandler(event_bus)
        key_handler = KeyExchangeHandler(event_bus)
        return Server(msg_handler, conn_handler, key_handler, event_bus)

class MovieServerDriver:
    def start():
        print("Starting")
        server = MovieServerBuilder().build()
        server.start()

class MovieConnectionHandler(ConnectionHandler):
    def __init__(self, event_bus: EventBus):
        super().__init__(event_bus)
        self.__movie_manager = MovieCacheManager()

    
    def on_change(self, event: Event):
        super().on_change(event)

        match event:
            case GetMovieRequestEvent():
                entries = self.__movie_manager.get_entries()
                data = GetMoviesResponseData(entries, event.get_request_id())
                msg = GetMoviesResponse(data)
                id = event.get_id()
                self._connections[id].send_to_client(msg)
            case AddMovieEvent():
                self.logInfo("Adding entry", event.get_entry().get_movie().get_name())
                self.__movie_manager.add_entry(event.get_entry())
            case DeleteMovieEvent(): 
                self.logInfo("Removing entry", event.get_entry().get_movie().get_name())
                self.__movie_manager.remove_entry(event.get_entry())
            case _:
                pass

    

    

if __name__ == "__main__":
    MovieServerDriver.start()