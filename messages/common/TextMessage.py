from messages.common.Serializable import Serializable

class TextMessage(Serializable):
    TextProperty = "text"

    def __init__(self, data: str | dict):
        if (isinstance(data, str)):
            self.__msg = data
        else:
            self.__msg = data[TextMessage.TextProperty]

    def get_msg(self) -> str:
        return self.__msg
    
    def to_map(self) -> dict:
        return {
            TextMessage.TextProperty: self.__msg
        }