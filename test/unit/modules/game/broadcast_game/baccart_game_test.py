import sys
sys.path.append("../../../../../modules/game")
sys.path.append("../../../../../modules/game/broadcast_game")

import unittest
from baccarat import *
from fsm import *
from poker import *

class baccaratTestCase(unittest.TestCase):
    # prepare work before every test
    def setUp(self):
        mygame = baccarat("test_baccart")

        playerlist = player_list()
        player = player_info("11", None)
        playerlist.add_player(player)
        setattr(mygame, 'player_list', playerlist)
        setattr(mygame, 'proxy_socket', None)

        self.myfsm = fsm()
        setattr(self.myfsm,'game',mygame)

        #for test ,step by step
        self.myfsm.add(init(-1))
        self.myfsm.add(wait_bet(-1))
        self.myfsm.add(player_card(-1))
        self.myfsm.add(banker_card(-1))
        self.myfsm.add(settle(-1))
        #myfsm.start("init")

    # clean work after every test
    def tearDown(self):
        pass

    def test_baccarat_state(self):

        self.myfsm.kick("init")
        self.myfsm.test_script("tie",["3_d","5_d","5_s","3_c"])
        self.assertEqual([],self.myfsm._current_state.game._poker.query("playerPoker",Poker.QUERY_POKER))
        self.assertEqual([],self.myfsm._current_state.game._poker.query("BankerPoker",Poker.QUERY_POKER))

        self.myfsm.next()
        self.assertEqual([],self.myfsm._current_state.game._poker.query("playerPoker",Poker.QUERY_POKER))
        self.assertEqual([],self.myfsm._current_state.game._poker.query("BankerPoker",Poker.QUERY_POKER))
        
        self.myfsm.next()
        self.assertEqual(["3_d"],self.myfsm._current_state.game._poker.query("playerPoker",Poker.QUERY_POKER))
        self.assertEqual([],self.myfsm._current_state.game._poker.query("BankerPoker",Poker.QUERY_POKER))

        self.myfsm.next()
        self.assertEqual(["3_d"],self.myfsm._current_state.game._poker.query("playerPoker",Poker.QUERY_POKER))
        self.assertEqual(["5_d"],self.myfsm._current_state.game._poker.query("BankerPoker",Poker.QUERY_POKER))

        self.myfsm.next()
        self.assertEqual(["3_d","5_s"],self.myfsm._current_state.game._poker.query("playerPoker",Poker.QUERY_POKER))
        self.assertEqual(["5_d"],self.myfsm._current_state.game._poker.query("BankerPoker",Poker.QUERY_POKER))

        self.myfsm.next()
        self.assertEqual(["3_d","5_s"],self.myfsm._current_state.game._poker.query("playerPoker",Poker.QUERY_POKER))
        self.assertEqual(["5_d","3_c"],self.myfsm._current_state.game._poker.query("BankerPoker",Poker.QUERY_POKER))

        self.myfsm.next()
        self.assertEqual("tie",self.myfsm._current_state.game._winstate)

        self.assertEqual([[8,"t"]], self.myfsm._current_state.game._history)


    #@unittest.skip("skipping")




if __name__ == '__main__':
    unittest.main()
