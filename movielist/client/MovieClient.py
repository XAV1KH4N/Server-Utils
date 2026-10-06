from common.RequestWorker import RequestWorker
from common.events.Events import EventHandler
from common.logging.Logger import Logger
from messages.common.Serializable import Requestable
from client.client import Client
from movielist.client.MovieServerConnectionHandler import MovieServerConnectionHandler
from movielist.common.MovieRequests import AddMovieData, AddMovieMessage, DeleteMovieMessage, GetMoviesRequest
from movielist.common.events.MovieEvents import GetMovieRequestEvent, GetMovieResponseEvent
from movielist.server.MovieMessageBuilder import MovieMessageBuilder

class MovieClient(Client, EventHandler): # Maybe use this instance?
    def __init__(self):
        super().__init__()
        self.__running = True
        self._event_bus.subscribe(self)
        self.start()

    def on_change(self, event):
        match event:
            case _:
                pass

    def create_connection_handler(self) -> None:
        self.logInfo("Creating Movie Server Connection Handler")
        return MovieServerConnectionHandler(self._event_bus, MovieMessageBuilder())

    def main_loop(self):
        while self.__running:
            self.__print_options()
            choice = input("-> ")
            valid, cleaned_choice = self.__validate_input(choice)
            if (valid):
                match cleaned_choice:
                    case 1:
                        self.__request_movies()
                    case 2:
                        self.__add_movie()
                    case 3:
                        self.__delete_movie()
                    case 4:
                        self.__running = False
                    case _:
                        self.logError("Missing implementation")

            else:
                self.logWarning("Invalid Message")

    def __add_movie(self):
        movie_name = input("Movie Name: ")
        username = "xavi"
        data = AddMovieData(movie_name, username)
        msg = AddMovieMessage(data)
        self._connection_handler.send_to_server_encrypted(msg)

    def __delete_movie(self):
        movie_name = input("Movie Name: ")
        msg = DeleteMovieMessage(movie_name)
        self._connection_handler.send_to_server_encrypted(msg)

    def __request_movies(self):

        class MovieWorker(RequestWorker):
            def get_request(self) -> Requestable:
                return GetMoviesRequest()

            def response_event_type(self): 
                return GetMovieResponseEvent

            def on_complete(inner_self, result: GetMovieResponseEvent) -> None:
                self.logInfo(f"Recieved {len(result.get_entries())} movie titles")
                s = ""
                for e in result.get_entries():
                    s += str((e.get_movie().get_name(), e.get_username())) + ""
                if s != "":
                    self.logInfo("Movies\n", s)

            def on_failure(inner_self) -> None:
                self.logError("Failed to recieve")

        self.logInfo("Requesting Movies")        
        self._connection_handler.request_to_worker(MovieWorker())

    def __validate_input(self, choice: str):
        valid = [1, 2, 3, 4]
        try:
            i = int(choice)      
            return (i in valid), i
        except:
            return False, -1

    def __print_options(self) -> None:
        print('''
        Options ... 
            (1) View Movies 
            (2) Add movie
            (3) Delete movie
            (4) Terminate
        ''')


class MovieClientDriver:
    def start():
        MovieClient()

if __name__ == "__main__":
    MovieClientDriver.start()