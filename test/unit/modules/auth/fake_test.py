import sys
sys.path.append("../../../../modules/auth")

import unittest
from mock import Mock
from fake import *


class AuthTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.name = "dyson"
        self.pw = "123"
        self.client_id = 123123

        self.client_login = {'cmd':"login","token":self.name+"_"+self.pw,'client_id':self.client_id}
  

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
        del mock_rsp['for_db']

        #rsp subset of b
        self.assertDictContainsSubset(rsp,mock_rsp)


if __name__ == '__main__':
    unittest.main()

