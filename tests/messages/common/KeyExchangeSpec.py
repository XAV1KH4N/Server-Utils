from unittest import TestCase, main

from RSA.RSAPublic import RSAPublicKeyReader
from RSA.RSAKeyPairGen import RSAKeyPairGen
from Server.handler.KeyExchangeHandler import ServerKeyExchangeHandler
from messages.keyExchange.KeyExchanges import KeyExchangeSupport

class TestKeyExchange(TestCase):

    def test_key_exchange(self):
       handler = KeyExchangeSupport()
       handler.set_up_this_y(5)
       handler.set_up(6, 13)
       Y = handler.Y()
       self.assertEqual(Y, 2)

    def test_key_server_exchange(self):
        handler = KeyExchangeSupport()
        handler.set_up_this_y(5)
        handler.set_up(6, 13)
        handler.set_up_other_y(9)
        ss = handler.K()
        self.assertEqual(ss, 3)

    def test_sign_key(self):
        handler = ServerKeyExchangeHandler()
        handler.set_up_this_y(5)
        handler.set_up(6, 13)
        handler.set_up_other_y(9)
        ss = handler.K()
        self.assertEqual(ss, 3)
    
        public_key = RSAPublicKeyReader(RSAKeyPairGen.PUBLIC_PATH).handler()
        
        msg = handler.Y_bytes()
        signature = handler.signed_Y()

        b = public_key.verify_message(msg, signature)
        self.assertTrue(b)

if __name__ == '__main__':
    main()