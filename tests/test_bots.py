import unittest
from bots.bot1.bot1 import Bot1
from bots.bot2.bot2 import Bot2
from bots.bot3.bot3 import Bot3

class TestBots(unittest.TestCase):
    def test_bot1(self):
        self.assertEqual(Bot1().respond('hi'), 'hi')

    def test_bot2(self):
        # Ensure returned string is a valid ISO date string
        t = Bot2().get_time()
        self.assertTrue('T' in t)

    def test_bot3(self):
        joke = Bot3().tell_joke()
        self.assertIn(joke, Bot3.JOKES)

if __name__ == '__main__':
    unittest.main()
