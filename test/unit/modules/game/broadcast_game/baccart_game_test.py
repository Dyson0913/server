import sys
sys.path.append("../../../../../modules/game")
sys.path.append("../../../../../modules/game/broadcast_game")

import unittest
from baccart_game import *
from fsm import *

class baccaratTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        mygame = baccarat("test_baccart")

        self.myfms = fms()
        self.myfms.add(State(init(mygame),1))
        self.myfms.add(State(wait_bet(mygame),1))
        self.myfms.add(State(player_card(mygame),2))
        self.myfms.add(State(banker_card(mygame),2))
        self.myfms.add(State(settle(mygame),1))
        #myfms.start("init")

    # clean work after every test
    def tearDown(self):
        pass

    def test_baccarat_state(self):

        self.myfms.kick("init")
        self.assertEqual("wait_bet",self.myfms._current_state._state_unit._next_state)
        self.assertEqual([],self.myfms._current_state._state_unit._game._player)
        self.assertEqual([],self.myfms._current_state._state_unit._game._banker)


    #@unittest.skip("skipping")

if __name__ == '__main__':
    unittest.main()
