from messages.common.Serlializable import Serializable
from messages.ConnectionStatus import ConnectionStatus

class UserLoginMessageData():
    def __init__(self, name, password):
        self.name = name
        self.password = password

class UserLoginMessage(Serializable):
    NameProperty = "name"
    PassProperty = "pass"

    def __init__(self, data):
        if (isinstance(data, UserLoginMessageData)):
            self.name = data.name
            self.password = data.password
        elif (isinstance(data, {})):
            self.name = data[UserLoginMessage.NameProperty]
            self.password = data[UserLoginMessage.PassProperty]
        else:
            self.name = ""
            self.password = ""

    def to_map(self) -> dict:
        return {
            UserLoginMessage.NameProperty: self.name,
            UserLoginMessage.PassProperty: self.password
        }
    

class UserLoginStatus(Serializable):
    StatusProperty = "status"

    def __init__(self, data):
        if (isinstance(data, ConnectionStatus)):
            self.status = data
        elif (isinstance(data, {})):
            self.status = data[UserLoginStatus.StatusProperty]
        else:
            self.status = ""

    def to_map(self) -> dict:
        return {
            UserLoginStatus.StatusProperty: self.status.name
        }
    