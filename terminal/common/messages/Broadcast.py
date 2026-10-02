from messages.common.Serializable import Serializable

class BroadcastMessage(Serializable):
    TextProperty = "text"

    def __init__(self, data: str | dict):
        if (isinstance(data, str)):
            self.__text = data
        elif (isinstance(data, dict)):
            self.__text = data[self.TextProperty]
        else:
            self.__text = ""

    def to_map(self):
        return {
            BroadcastMessage.TextProperty: self.__text
        }
    
    def getText(self):
        return self.__text