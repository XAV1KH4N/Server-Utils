from unittest import TestCase, main
from messages.common.KeyExchangeMessage import KeyExchangeData, KeyExchangeInitMessage

class TestKeyExchangeMessages(TestCase):

   def test_key_exchange_message(self):
       y = 13
       b = 4
       p = 9
       sign = b'1234'

       data = KeyExchangeData(y, sign, b, p)
       msg = KeyExchangeInitMessage(data)

       map = msg.to_map()
       new_mg = KeyExchangeInitMessage(map)

       self.assertEqual(new_mg.get_base(), b)
       self.assertEqual(new_mg.get_Y(), y)
       self.assertEqual(new_mg.get_signature(), sign)
       self.assertEqual(new_mg.get_prime(), p)


if __name__ == '__main__':
    main()