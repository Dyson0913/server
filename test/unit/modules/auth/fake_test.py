import sys
sys.path.append("../../../../modules/auth")

import unittest
import json
from mock import Mock
from fake import *


class AuthTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.name = "dyson"
        self.pw = "123"
        self.client_id = 123123

        self.client_login = {'cmd':"login","token":self.name+"_"+self.pw,'client_id':self.client_id}
        self.client_try_login = {'cmd':"try_login","token":self.name+"_"+self.pw,'client_id':self.client_id}
        
        self.close_nodata = {'cmd':"self_close",'uuid':self.name}

    # clean work after every test
    def tearDown(self):
        pass

    def test_first_login(self):
        rsp = {'state':"login_ok","cmd":"login","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = None
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.client_login,[mock_push_socket,mock_db_socket])
       
        #for_db dynamic generate ,test later 
        #del mock_rsp['for_db']

        #rsp subset of b
        self.assertDictContainsSubset(rsp,mock_rsp)
        
        #try again login
        try_rsp = {'state':"login_ok","cmd":"try_login","key":self.name}
        mock_try_rsp = normal_handle(self.client_try_login,[mock_push_socket,mock_db_socket])
        self.assertDictContainsSubset(try_rsp,mock_try_rsp)

    def test_success_login(self):

        rsp = {'state':"login_ok","cmd":"login","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"self_close",'for_db':{'playerinfo':{'pw':self.pw}}})
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.client_login,[mock_push_socket,mock_db_socket])

        self.assertDictContainsSubset(rsp,mock_rsp)

        try_rsp = {'state':"login_ok","cmd":"try_login","key":self.name}
        mock_try_rsp = normal_handle(self.client_try_login,[mock_push_socket,mock_db_socket])
        self.assertDictContainsSubset(try_rsp,mock_try_rsp)


    def test_multi_login(self):

        rsp = {'state':"login_fail","cmd":"login","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"lobby",'for_db':{'playerinfo':{'pw':self.pw}}})
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.client_login,[mock_push_socket,mock_db_socket])

        self.assertDictContainsSubset(rsp,mock_rsp)
        self.assertEqual("alreay login on other device!",mock_rsp['reason'])


        try_rsp = {'state':"login_fail","cmd":"try_login","key":self.name}
        mock_try_rsp = normal_handle(self.client_try_login,[mock_push_socket,mock_db_socket])
        self.assertDictContainsSubset(try_rsp,mock_try_rsp)

    def test_pwError_login(self):

        rsp = {'state':"login_fail","cmd":"login","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"lobby",'for_db':{'playerinfo':{'pw':"errorpw"}}})
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.client_login,[mock_push_socket,mock_db_socket])

        self.assertDictContainsSubset(rsp,mock_rsp)
        self.assertEqual("password error",mock_rsp['reason'])

    def test_close_not_exist_login(self):

        rsp = {'uuid':self.name,"cmd":"self_close","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = None
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.close_nodata,[mock_push_socket,mock_db_socket])
        self.assertDictContainsSubset(rsp,mock_rsp)

    def test_close_in_lobby_login(self):

        rsp = {'state':"self_close",'uuid':self.name,"cmd":"self_close","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"lobby_waitting",'playing_module':"slot_1",'playing_group':1})
        mock_db_socket.save.retrun_value = None
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.close_nodata,[mock_push_socket,mock_db_socket])
        self.assertDictContainsSubset(rsp,mock_rsp)

    def test_close_in_game_login(self):

        rsp = {'module':"slot_1",'game_id':1,'uuid':self.name,"cmd":"lost_connect","key":self.name}

	mock_db_socket = Mock()
        mock_db_socket.get.return_value = json.dumps({'state':"in_game",'playing_module':"slot_1",'playing_group':1})
	mock_push_socket = Mock()
        mock_rsp = normal_handle(self.close_nodata,[mock_push_socket,mock_db_socket])
        self.assertDictContainsSubset(rsp,mock_rsp)


if __name__ == '__main__':
    unittest.main()

