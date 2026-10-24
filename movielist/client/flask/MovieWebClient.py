from common.RequestWorker import RequestWorker
from common.events.Events import EventHandler
import threading
from common.logging.Logger import Logger
from messages.common.Serializable import Requestable
from client.client import Client
from movielist.client.MovieClient import MovieClient
from movielist.client.MovieServerConnectionHandler import MovieServerConnectionHandler
from movielist.common.Movie import MovieEntry
from movielist.common.MovieRequests import AddMovieData, AddMovieMessage, DeleteMovieMessage, GetMoviesRequest
from movielist.common.events.MovieEvents import GetMovieRequestEvent, GetMovieResponseEvent
from movielist.server.MovieMessageBuilder import MovieMessageBuilder
from flask import Flask, render_template, request
from flask_classful import FlaskView, route

class IndexConfig:
    def __init__(self, movies: list[MovieEntry], usernames: list[str]):
        self.movies: list[MovieEntry] = movies
        self.usernames = usernames

    def get_usernames(self) -> list[str]:
        return self.usernames

    def get_movies(self) -> list[MovieEntry]:
        return self.movies

    def get_movies_str(self):
        return str(len(self.movies))

# This means multiple website will use this one instance, good for apps, bad for websites
# Need a better architecture
# Web sockets?
# Remove the need for a lot of the client stuff...? Not sure, need the diffe hellman protocol and stuff
class MoveWebClientInstance(Client, EventHandler): 
    def __init__(self):
        self.logDebug("STARTING")
        super().__init__()
        self.__running = True
        self._event_bus.subscribe(self)
        self.config = IndexConfig([], ["xavi", "maya"])
    
        connection_thread = threading.Thread(target=self.start, daemon=True)
        connection_thread.start()

    def start(self):
        self._connection_handler.persist_connection(self.main_loop)

    def refresh_movies(self) -> None:
        self.__request_movies()

    def on_change(self, event):
        match event:
            case _:
                pass

    def create_connection_handler(self) -> None:
        self.logInfo("Creating Movie Server Connection Handler")
        return MovieServerConnectionHandler(self._event_bus, MovieMessageBuilder())

    def main_loop(self):
        self.__request_movies()

    def add_movie_entry(self, movie_name: str, username: str):
        data = AddMovieData(movie_name, username)
        msg = AddMovieMessage(data)
        self._connection_handler.send_to_server_encrypted(msg)

    def delete_movie_entry(self, username: str):
        msg = DeleteMovieMessage(username)
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
                    self.config.movies = result.get_entries()

            def on_failure(inner_self) -> None:
                self.logError("Failed to recieve")

        self.logInfo("Requesting Movies")        
        self._connection_handler.request_to_worker(MovieWorker())
    

class MovieWebClient(FlaskView):
    client = MoveWebClientInstance()
   
    def index(self):
        # http://localhost:5000/
        return render_template('index.html', config = self.client.config)# Maybe show a loading page...?

    @route('/submit', methods=['POST'])
    def add_movie(self):
        # Handle the form submission automatically when 'POST' is received
        movie_name = request.form.get('movie_name')
        username = request.form.get('usernmae')
        self.client.add_movie_entry(movie_name, username)
        self.client.refresh_movies()
        return render_template('index.html', config = self.client.config)# Maybe show a loading page...?

    @route('/submit', methods=['POST'])
    def delete_movie(self):
        # Handle the form submission automatically when 'POST' is received
        movie_name = request.form.get('movie_name')
        self.client.delete_movie_entry(movie_name)
        self.client.refresh_movies()
        # Redirect to avoid duplicate submissions on page refresh
        return self.index()


class MovieClientDriver:
    def start():
        MovieClient().start()

if __name__ == "__main__":
    MovieClientDriver.start()