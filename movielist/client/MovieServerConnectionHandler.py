from client.connections.ServerConnectionHandler import ServerConnectionHandler
from common.events.Events import Event
from messages.common.Serializable import Serializable
from movielist.common.MovieRequests import GetMoviesResponse
from movielist.common.events.MovieEvents import GetMovieResponseEvent
from movielist.server.MovieMessageBuilder import MovieMessageBuilder

class MovieServerConnectionHandler(ServerConnectionHandler):
    def __init__(self, event_bus, message_builder: MovieMessageBuilder):
        super().__init__(event_bus, message_builder)

    def on_change(self, event: Event) -> None:
        super().on_change(event)

    def _handle_msg(self, msg: Serializable) -> None:
        super()._handle_msg(msg)
        self.logDebug("Handling", msg)
        match msg:
            case GetMoviesResponse():
                self.logInfo("Recieved Got Movie Reponse")
                entries = msg.get_entries()
                request_id = msg.get_request_id()
                self._event_bus.publish(GetMovieResponseEvent(request_id, entries))
            case _:
                pass

        
    