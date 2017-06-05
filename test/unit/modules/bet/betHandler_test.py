#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,parentdir)

import sys
sys.path.append("../../../../modules/bet")

import unittest
import json
from mock import Mock
from betHandler import *


class betTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.bet = {'cmd': "bet", "uuid":"111","game_id":"ba_1", 'bet':[{'type':1,'amount':100},{'type':2,'amount':200}]}

    # clean work after every test
    def tearDown(self):
        pass

    def test_bet(self):

        rsp = {'state':"bet_ok", "uuid":"111"}

        mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"self_close",'for_db':{'playerinfo':{"credit": {"total":10000,"ba_1":2000}}}})
        mock_push_socket = Mock()
        mock_rsp = normal_handle(self.bet, [mock_push_socket, mock_db_socket])
     #   self.assertDictContainsSubset(rsp, mock_rsp)

    #    self.assertEqual(len(self.fsm._all_state), 2)


if __name__ == '__main__':
    unittest.main()
