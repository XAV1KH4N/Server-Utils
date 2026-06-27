from messages.Serlializable import Serializable

class SendAllMessage(Serializable):
    TextProperty = "text"

    def __init__(self, data):
        if (isinstance(data, str)):
            self.text = data
        elif (isinstance(data, dict)):
            self.text = data[self.TextProperty]
        else:
            self.text = ""

    def toMap(self):
        return {
            SendAllMessage.TextProperty: self.text
        }

class SendTextMessage(Serializable):
    TextProperty = "text"

    def __init__(self, data):
        if (isinstance(data, str)):
            self.__text = data
        elif (isinstance(data, dict)):
            self.__text = data[self.TextProperty]
        else:
            self.__text = ""

    def toMap(self):
        return {
            SendTextMessage.TextProperty: self.__text
        }
    
    def getText(self):
        return self.__text