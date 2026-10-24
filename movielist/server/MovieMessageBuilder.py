from common.logging.Logger import Logger
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Messages import Message
from messages.common.Serializable import Serializable
from movielist.common.MovieRequests import AddMovieMessage, DeleteMovieMessage, GetMoviesRequest, GetMoviesResponse

class MovieMessageBuilder(MessageBuilder, Logger):
    def extract_message(self, message: Message) -> Serializable:
        self.logInfo(message.get_class_name())
        msg = super().extract_message(message)
        if (msg != None):
            return msg

        msg_map = message.get_msg_map()
        match message.get_class_name():
            case GetMoviesRequest.__name__:
                return GetMoviesRequest(msg_map)
            case GetMoviesResponse.__name__:
                return GetMoviesResponse(msg_map)
            case AddMovieMessage.__name__:
                return AddMovieMessage(msg_map)
            case DeleteMovieMessage.__name__:
                return DeleteMovieMessage(msg_map)
            case _:
                self.logError("Unexpected message wrapped") 
                return None