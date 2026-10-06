import json

from messages.common.Serializable import Requestable, Responsable, Serializable
from movielist.common.Movie import MovieEntry

class GetMoviesRequest(Requestable):
    def __init__(self, data: dict[str, str] = {}):
        super().__init__()

        if len(data) == 0:
            self.__request_id = self.generate_request_id()
        else:
            self.__request_id = data[Requestable.RequestIdProperty]

    def to_map(self):
        return {
            Requestable.RequestIdProperty : self.__request_id
        }

    def get_request_id(self) -> str:
        return self.__request_id

class GetMoviesResponseData:

    def __init__(self, entries: list[MovieEntry], request_id: str):
        self.__entries = entries
        self.__request_id = request_id

    def get_entries(self) -> list[MovieEntry]:
        return self.__entries

    def get_request_id(self) -> str:
        return self.__request_id

class GetMoviesResponse(Responsable):
    EntriesProperty = "entries"

    def __init__(self, data: GetMoviesResponseData | dict[str, str]):

        if (isinstance(data, GetMoviesResponseData)):
            self.__entries = data.get_entries()
            self.__request_id = data.get_request_id()
        else:
            json_data = data[GetMoviesResponse.EntriesProperty]
            dicts : list[dict[str, str]]= json.loads(json_data)
            entries = [MovieEntry(dct) for dct in dicts]
            self.__entries = entries
            self.__request_id = data[Requestable.RequestIdProperty]

    def to_map(self):
        lst = [entry.to_dict() for entry in self.__entries]
        json_data = json.dumps(lst)
        return {
            Requestable.RequestIdProperty : self.__request_id,
            GetMoviesResponse.EntriesProperty : json_data
        }

    def get_entries(self) -> list[MovieEntry]:
        return self.__entries

    def get_request_id(self) -> str:
        return self.__request_id

class AddMovieData:
    def __init__(self, movie_name: str, username: str):
        self.__movie_name = movie_name
        self.__username = username

    def get_movie_name(self) -> str:
        return self.__movie_name

    def get_username(self) -> str:
        return self.__username

class AddMovieMessage(Serializable):
    MovieNameProperty = "movie_name"
    UsernameProperty = "username"

    def __init__(self, data: AddMovieData | dict[str, str]):
        if isinstance(data, AddMovieData):
            self.__movie_name = data.get_movie_name()
            self.__username = data.get_username()
        else:
            self.__movie_name = data[AddMovieMessage.MovieNameProperty]
            self.__username = data[AddMovieMessage.UsernameProperty]

    def get_movie_name(self) -> str:
        return self.__movie_name

    def get_username(self) -> str:
        return self.__username

    def to_map(self):
        return {
            AddMovieMessage.MovieNameProperty: self.__movie_name,
            AddMovieMessage.UsernameProperty: self.__username 
        }

class DeleteMovieMessage(Serializable):
    MovieNameProperty = "movie_name"

    def __init__(self, data: str | dict[str, str]):
        if isinstance(data, str):
            self.__movie_name = data
        else:
            self.__movie_name = data[AddMovieMessage.MovieNameProperty]

    def get_movie_name(self) -> str:
        return self.__movie_name

    def to_map(self):
        return {
            DeleteMovieMessage.MovieNameProperty : self.__movie_name
        }
