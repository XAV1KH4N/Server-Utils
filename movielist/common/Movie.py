import json

class Movie:
    NameProperty = "name"

    def __init__(self, data: str | dict[str, str]):
        if (isinstance(data, str)):
            self.__name = data
        else:
            self.__name = data[Movie.NameProperty]

    def get_name(self) -> str:
        return self.__name

    def to_dict(self) -> dict[str, str]:
        return {
            Movie.NameProperty : self.__name
        }

    def __eq__(self, other):
        if isinstance(other, Movie):
            return self.__name == other.get_name()
        return False

class MovieEntryData:
    def __init__(self, movie: Movie, username: str):
        self.__movie = movie
        self.__username = username

    def get_movie(self) -> Movie:
        return self.__movie

    def get_username(self) -> str:
        return self.__username

class MovieEntry:
    MovieProperty = "movie"
    UsernameProperty = "username"

    def __init__(self, data: MovieEntryData | dict[str, str]):
        if (isinstance(data, MovieEntryData)):
            self.__movie = data.get_movie()
            self.__username = data.get_username()
        else:
            movie_json = data[MovieEntry.MovieProperty]
            dct = json.loads(movie_json)
            movie = Movie(dct)
            self.__movie = movie
            self.__username = data[MovieEntry.UsernameProperty]

    def get_movie(self) -> Movie:
        return self.__movie

    def get_username(self) -> str:
        return self.__username

    def to_dict(self) -> dict[str, str]:
        movie_json = json.dumps(self.__movie.to_dict())
        return {
            MovieEntry.MovieProperty : movie_json,
            MovieEntry.UsernameProperty : self.__username 
        }

    def __eq__(self, other):
        if isinstance(other, MovieEntry):
            return self.__username == other.get_username() and self.__movie == other.get_movie()
        return False
