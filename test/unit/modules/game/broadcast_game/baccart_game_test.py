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

        self.myfsm = fsm()
        setattr(self.myfsm,'game',mygame)
        self.myfsm.add(init(1))
        self.myfsm.add(wait_bet(5))
        self.myfsm.add(player_card(2))
        self.myfsm.add(banker_card(1))
        self.myfsm.add(settle(1))
        #myfsm.start("init")

    # clean work after every test
    def tearDown(self):
        pass

    def test_baccarat_state(self):

        self.myfsm.kick("init")
        self.myfsm.test_script("tie",["3d","5d","5s","3c"])
        self.assertEqual([],self.myfsm._current_state.game._player)
        self.assertEqual([],self.myfsm._current_state.game._banker)

        self.myfsm.next()
        self.assertEqual([],self.myfsm._current_state.game._player)
        self.assertEqual([],self.myfsm._current_state.game._banker)
        
        self.myfsm.next()
        self.assertEqual(["3d"],self.myfsm._current_state.game._player)
        self.assertEqual([],self.myfsm._current_state.game._banker)

        self.myfsm.next()
        self.assertEqual(["3d"],self.myfsm._current_state.game._player)
        self.assertEqual(["5d"],self.myfsm._current_state.game._banker)

        self.myfsm.next()
        self.assertEqual(["3d","5s"],self.myfsm._current_state.game._player)
        self.assertEqual(["5d"],self.myfsm._current_state.game._banker)

        self.myfsm.next()
        self.assertEqual(["3d","5s"],self.myfsm._current_state.game._player)
        self.assertEqual(["5d","3c"],self.myfsm._current_state.game._banker)

        self.myfsm.next()
        self.assertEqual("tie",self.myfsm._current_state.game._win)


    #@unittest.skip("skipping")

if __name__ == '__main__':
    unittest.main()
