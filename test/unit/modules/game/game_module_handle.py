import sys
sys.path.append("../../../../modules/game")

import unittest
from mock import Mock

class mockTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        pass # self.poker = Poker()

    # clean work after every test
    def tearDown(self):
        pass #self.poker = None

    def test_remain(self):

        my_mock = Mock()
        my_mock.my_method.return_value = "hello"
        self.assertEqual("hello", my_mock.my_method())


if __name__ == '__main__':
    unittest.main()
