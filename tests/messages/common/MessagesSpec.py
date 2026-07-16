import base64
from unittest import TestCase, main
from messages.common.Messages import EncryptedMessage, EncryptedMessageData, Message
from common.EncyptUtils import EncryptUtils

class TestMessageClasses(TestCase):

    def test_encrypted_message(self):
        bs = b'1234'
        class_name = "TestClassName"
        data = EncryptedMessageData(bs, class_name)
        msg = EncryptedMessage(data)
        map = msg.to_map()
        
        final_map = {
            EncryptedMessage.CipherProperty : base64.b64encode(bs).decode(EncryptUtils.ENCODE_TYPE),
            EncryptedMessage.ClassNameProperty: class_name
        }

        self.assertEqual(map, final_map)

    def test_message_class_name(self):
        bs = b'abc'
        class_name = "AnotherTestClassName"

        enc_msg = EncryptedMessage(EncryptedMessageData(bs, class_name))
        msg = Message(enc_msg)

        msg_map = msg.to_map()
        recreated_msg = Message(msg_map).getMsgMap()
        recreated_enc_msg = EncryptedMessage(recreated_msg)

        self.assertEqual(recreated_enc_msg.getClassName(), "AnotherTestClassName")

    def test_encrypted_msg_build(self):
        bs = b'abc'
        class_name = "AnotherTestClassName"

        enc_map = EncryptedMessage(EncryptedMessageData(bs, class_name)).to_map()
        enc = EncryptedMessage(enc_map)

        self.assertEqual(enc.getCipherBytes(), bs)
        self.assertEqual(enc.getClassName(), class_name)
        
if __name__ == '__main__':
    main()