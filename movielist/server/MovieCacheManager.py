import json
from Server.filehandler.FileHandler import FileHandler
from movielist.common.Movie import Movie, MovieEntry

class MovieCacheManager:
    __FileName = "MovieList"

    def __init__(self, override_name = ""):
        file_name = MovieCacheManager.__FileName
        if (override_name != ""):
            file_name = override_name

        self.__entries: list[MovieEntry] = []
        self.__filehandler = FileHandler(file_name)
        self.init_cache()

    def init_cache(self):
        text = self.__filehandler.read_raw()
        if (text == ""):
            return
        json_dict: list[dict[str, str]] = json.loads(text)
        self.__entries = [MovieEntry(dct) for dct in json_dict]

    def remove_entry(self, movie: MovieEntry) -> None:
        if movie in self.__entries:
            self.__entries.remove(movie)
            return True
        else:
            return False

    def add_entry(self, movie: MovieEntry) -> None:
        self.__entries.append(movie)
        self.write_to_file()

    def get_entries(self) -> list[MovieEntry]:
        return self.__entries

    def get_entries_count(self) -> list[MovieEntry]:
        return len(self.__entries)

    def get_movies(self) -> list[Movie]:
        return [entry.get_movie() for entry in self.__entries]

    def to_json(self) -> str:
        dicts = [entry.to_dict() for entry in self.__entries]
        json_data = json.dumps(dicts)
        return json_data

    def write_to_file(self) -> None:
        self.__filehandler.write(self.to_json())