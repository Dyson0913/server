import sys
sys.path.append("../../../../modules/lobby")

import unittest
import json
from mock import Mock
from normal import *


class NormalLobbyTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.name = "dyson"
        self.pw = "123"
        self.client_id = 123123

        self.client_request_gamelist = {'cmd':"request_gamelist","uuid":self.name}

    # clean work after every test
    def tearDown(self):
        pass

    def test_request_gamelist(self):
        rsp = {'state':"lobby_waitting","gamelist":[{"game":"hope"},{"game":"ThreeKingdoms"}],"key":self.name}

	mock_db = Mock()
    #    mock_db.save.return_value = None
        mock_db.get.return_value = json.dumps({"app":[{"game":"hope"},{"game":"ThreeKingdoms"}]})
        mock_rsp = normal_handle(self.client_request_gamelist,[None,mock_db])
       
        self.assertDictContainsSubset(rsp,mock_rsp)
    #    self.assertDictEqual(rsp,mock_rsp)
        
if __name__ == '__main__':
    unittest.main()

