from unittest import TestCase, main
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder
from messages.common.Messages import EncryptedMessage
from messages.common.MessageBuilder import MessageBuilder
from messages.common.Serializable import Serializable, SerializerBuilder

class TestMessageBuilder(TestCase):

    def test_message_rebuild(self):
        enc_builder = EncryptMessageBuilder(11, TestSerializerBuilder())
        msg = TestMessage("abcd")
        enc_msg = enc_builder.build_message(msg)

        msg_builder = MessageBuilder()
        encoded_msg = msg_builder.build_message_bytes(enc_msg)

        rebuilt_msg = msg_builder.rebuild_message(encoded_msg)
        
        is_instance = isinstance(rebuilt_msg, EncryptedMessage)
        self.assertTrue(is_instance)
        if (is_instance):
            og_msg = enc_builder.recreate_message(rebuilt_msg)
            is_og_instance = isinstance(og_msg, TestMessage)
            self.assertTrue(is_og_instance)
            if (is_og_instance):
                self.assertEqual(og_msg.getData(), "abcd")
            

class TestSerializerBuilder(SerializerBuilder):

    def build_message(self, map: dict, class_name: str) -> Serializable: 
        match class_name:
            case "TestMessage" : return TestMessage(map)
            case _: raise Exception("Unfound message")


class TestMessage(Serializable):
    DataProperty = "data" 

    def __init__(self, data: str | dict):
        if (isinstance(data, str)):
            self.__data = data
        else:
            self.__data = data[TestMessage.DataProperty]

    def to_map(self) -> dict:
        return {
            TestMessage.DataProperty : self.__data
        }
    
    def getData(self) -> str:
        return self.__data

if __name__ == '__main__':
    main()