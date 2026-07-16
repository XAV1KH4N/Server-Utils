from messages.common.MessageBuilder import MessageBuilder

class MessageHandler:
    def __init__(self):
        self.__builder = MessageBuilder()

    def handleRaw(self, raw_data: bytes) -> None:
        msg = self.__builder.rebuild_message(raw_data)
        match msg:
            case _: raise Exception("Message could not be reconstucted")

    

