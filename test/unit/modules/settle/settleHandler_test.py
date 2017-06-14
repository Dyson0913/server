#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,parentdir)

import sys
sys.path.append("../../../../modules/settle")

import unittest
import json
from mock import Mock
from settleHandler import *


class betTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.settle_banker_win = {'cmd': "settle","game_id":"ba_1","settle_player_id":[123,456,789],'game_result':[1.95,0,0,0,0]}
        self.settle_player_win = {'cmd': "settle","game_id":"ba_1","settle_player_id":[123,456,789],'game_result':[0,2,0,0,0]}
        self.settle_tie = {'cmd': "settle","game_id":"ba_1","settle_player_id":[123,456,789],'game_result': [0,0,9,0,0]}

    # clean work after every test
    def tearDown(self):
        pass

    def test_banker_win(self):
        mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"self_close",'for_db':{'bill':{'game_id':"ba_1",'bet':[{'amount':100,'type':0},{'amount':100,'type':1}]},'playerinfo':{"credit": {"total":10000,"ba_1":2000}}}})
        mock_push_socket = Mock()
        mock_rsp = normal_handle(self.settle_banker_win, [mock_push_socket, mock_db_socket])

    #@unittest.skip("testing skipping")
    def test_player_win(self):
        mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"self_close",'for_db':{'bill':{'game_id':"ba_1",'bet':[{'amount':100,'type':0},{'amount':100,'type':1}]},'playerinfo':{"credit": {"total":10000,"ba_1":2000}}}})
        mock_push_socket = Mock()
        mock_rsp = normal_handle(self.settle_player_win, [mock_push_socket, mock_db_socket])

#    @unittest.skip("testing skipping")
    def test_tie_win(self):
        mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"self_close",'for_db':{'bill':{'game_id':"ba_1",'bet':[{'amount':100,'type':0},{'amount':100,'type':2}]},'playerinfo':{"credit": {"total":10000,"ba_1":2000}}}})
        mock_push_socket = Mock()
        mock_rsp = normal_handle(self.settle_tie, [mock_push_socket, mock_db_socket])

    def test_loseConnect_settle_(self):
        mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state': "self_close", 'for_db': {
            'bill': {'game_id': "ba_1", 'bet': [{'amount': 100, 'type': 1}]},
            'playerinfo': {"credit": {"total": 10000}}}})
        mock_push_socket = Mock()
        mock_rsp = normal_handle(self.settle_player_win, [mock_push_socket, mock_db_socket])

if __name__ == '__main__':
    unittest.main()
