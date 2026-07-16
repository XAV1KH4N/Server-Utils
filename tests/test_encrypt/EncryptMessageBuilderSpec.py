from unittest import TestCase, main
from ecrypt.EncryptMessageBuilder import EncryptMessageBuilder
from messages.common.Messages import EncryptedMessage, EncryptedMessageData
from messages.common.Serlializable import Serializable, SerializerBuilder

class TestEncryptedMessageBuilderMethods(TestCase):

    def test_message_builder(self):
        bs = b'1234'
        class_name = "TestClassName"
        data = EncryptedMessageData(bs, class_name)
        msg = EncryptedMessage(data)

        builder = EncryptMessageBuilder(17, TestSerializerBuilder())
        wrapper = builder.build_message(msg)
        self.assertEqual(wrapper.getClassName(), "EncryptedMessage")

    def test_message_rebuilder(self):
        data = TestMessage("1234")

        builder = EncryptMessageBuilder(45, TestSerializerBuilder())
        wrapper = builder.build_message(data)

        og_msg = builder.recreate_message(wrapper)

        is_og_instance = isinstance(og_msg, TestMessage)
        self.assertTrue(is_og_instance)
        if (is_og_instance):
                self.assertEqual(og_msg.getData(), "1234")
            

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