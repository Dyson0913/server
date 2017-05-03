#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,parentdir)

import sys
sys.path.append("../../../../modules/game")

import unittest

from mock import Mock
from fsm import *


class fsmTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.fsm = fsm()

        mock_game = Mock()
        setattr(self.fsm,'game',mock_game)

	self.mock_init_status = Mock()
        self.mock_init_status.name.return_value = "mock_init"
#        self.mock

        print self.mock_init_status.name
	self.mock_round_status = Mock()
        self.mock_round_status.name.return_value = "mock_round"
        #mygame = baccarat("test_baccart")
        #setattr(self.myfms,'app',mygame)                
        #self.myfms.add(init(1))

    # clean work after every test
    def tearDown(self):
        self.fsm = None

    def test_add_state(self):
       
        self.fsm.add(self.mock_init_status)
        self.fsm.add(self.mock_round_status)

        self.assertEqual(len(self.fsm._all_state), 2)

    def test_start_state(self):
       
        self.fsm.add(self.mock_init_status)
        self.fsm.add(self.mock_round_status)

        self.assertEqual(self.fsm.start("mock_init"),True)


if __name__ == '__main__':
    unittest.main()
