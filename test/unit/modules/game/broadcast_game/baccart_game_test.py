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
        setattr(self.myfms,'app',mygame)
        self.myfms.add(init(1))
        self.myfms.add(wait_bet(5))
        self.myfms.add(player_card(2))
        self.myfms.add(banker_card(1))
        self.myfms.add(settle(1))
        #myfms.start("init")

    # clean work after every test
    def tearDown(self):
        pass

    def test_baccarat_state(self):

        self.myfms.kick("init")
        self.myfms.test_script("tie",["3d","5d","5s","3c"])
        self.assertEqual([],self.myfms._current_state.app._player)
        self.assertEqual([],self.myfms._current_state.app._banker)

        self.myfms.next()
        self.assertEqual([],self.myfms._current_state.app._player)
        self.assertEqual([],self.myfms._current_state.app._banker)
        
        self.myfms.next()
        self.assertEqual(["3d"],self.myfms._current_state.app._player)
        self.assertEqual([],self.myfms._current_state.app._banker)

        self.myfms.next()
        self.assertEqual(["3d"],self.myfms._current_state.app._player)
        self.assertEqual(["5d"],self.myfms._current_state.app._banker)

        self.myfms.next()
        self.assertEqual(["3d","5s"],self.myfms._current_state.app._player)
        self.assertEqual(["5d"],self.myfms._current_state.app._banker)

        self.myfms.next()
        self.assertEqual(["3d","5s"],self.myfms._current_state.app._player)
        self.assertEqual(["5d","3c"],self.myfms._current_state.app._banker)

        self.myfms.next()
        self.assertEqual("tie",self.myfms._current_state.app._win)


    #@unittest.skip("skipping")

if __name__ == '__main__':
    unittest.main()
