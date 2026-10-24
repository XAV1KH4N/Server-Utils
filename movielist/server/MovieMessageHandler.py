from Server.handler.MessageHandler import MessageHandler
from common.events.ConnectionId import ConnectionID
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import Message
from messages.common.Serializable import Serializable
from movielist.common.Movie import MovieEntry, MovieEntryData, Movie
from movielist.common.MovieRequests import AddMovieMessage, GetMoviesRequest
from movielist.common.events.MovieEvents import AddMovieEvent, GetMovieRequestEvent
from movielist.server.MovieMessageBuilder import MovieMessageBuilder

class MovieMessageHandler(MessageHandler):

    def __init__(self, event_bus):
        super().__init__(event_bus)

    def _create_message_builder(self) -> MessageBuilder:
        return MovieMessageBuilder()

    def handle_msg(self, msg: Serializable, id: ConnectionID):
        handled = super().handle_msg(msg, id)

        if (handled):
            return True

        match msg:
            case GetMoviesRequest():
                request_id = msg.get_request_id()
                self.event_bus.publish(GetMovieRequestEvent(request_id, id))
            case AddMovieMessage():
                username = msg.get_username()
                moviename = msg.get_movie_name()
                entry = MovieEntry(MovieEntryData(Movie(moviename), username))
                self.event_bus.publish(AddMovieEvent(entry))
            case _ :
                self.logError("Unhandled client message", msg.__class__.__name__) 
                return False
        return True