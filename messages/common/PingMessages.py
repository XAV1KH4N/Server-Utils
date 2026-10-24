from messages.common.Serializable import Requestable, Responsable


class PingMessage(Requestable):

    def __init__(self, data: dict[str, str] = {}):
        if (len(data) == 0):
            self.__request_id = self.generate_request_id()
        else:
            self.__request_id = data[Requestable.RequestIdProperty]

    def get_request_id(self):
        return self.__request_id

    def to_map(self) -> dict:
        return {
            Requestable.RequestIdProperty : self.__request_id
        }

class PongMessage(Responsable):

    def __init__(self, data: str | dict[str, str]):
        if (isinstance(data, str)):
            self.__request_id = data
        else:
            self.__request_id = data[Requestable.RequestIdProperty]            

    def get_request_id(self):
        return self.__request_id

    def to_map(self) -> dict:
        return {
            Requestable.RequestIdProperty : self.__request_id
        }