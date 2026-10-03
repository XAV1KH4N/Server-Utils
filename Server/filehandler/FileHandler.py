import os, json

class FileHandler:

    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.__root_path = self.get_root_path() 
        self.init_file()

    def init_file(self) -> None:
        if (not self.file_exists()):
            with open(f"{self.full_file_path()}", "w") as file:
                file.write("")        

    def file_exists(self) -> bool:
        return os.path.isfile(self.full_file_path())

    def remove_file(self) -> None:
        os.remove(self.full_file_path())

    def get_root_path(self) -> str:
        return os.path.dirname(os.path.abspath(__file__))

    def full_file_path(self) -> str:
        return f"{self.__root_path}/{self.__file_name}.txt"

    def write(self, text) -> None:
        with open(f"{self.full_file_path()}", "w") as file:
            file.write(text + "\n")

    def append(self, text) -> None:
        with open(f"{self.full_file_path()}", "a") as file:
            file.write(text + "\n")

    def read_raw(self) -> str:
        text = ""
        with open(f"{self.full_file_path()}", "r") as file:
            text = file.read()
        return text

    def read(self) -> list[str]:
        return self.read_raw().splitlines()
