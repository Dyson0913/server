import sys
sys.path.append("../..")

import unittest
from poker import *
import BPgame_paytable
from BPgame_paytable import *

class DealerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        pass

    # clean work after every test
    def tearDown(self):
        pass

    def test_baccarat_table(self):
        winstate = BPgame_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        self.assertEqual([0,1.95,0,0,0,0],BPgame_paytable.Baccarat_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(Baccarat_player,ba_odds_1)
        self.assertEqual([0,0,2,0,0,0],BPgame_paytable.Baccarat_paytable(winstate))

        winstate = ""
        winstate +=  BPgame_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
        self.assertEqual([1,1,1,9,1,1],BPgame_paytable.Baccarat_paytable(winstate))

        #multi winstate
        winstate = ""
        winstate = BPgame_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        winstate +=  BPgame_paytable.combine_winstate(Baccarat_banker_pair,ba_odds_11)
        self.assertEqual([0,1.95,0,0,12,0],BPgame_paytable.Baccarat_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        winstate += BPgame_paytable.combine_winstate(Baccarat_banker_pair,ba_odds_11)
        winstate += BPgame_paytable.combine_winstate(Baccarat_player_pair,ba_odds_11)
        self.assertEqual([0,1.95,0,0,12,12],BPgame_paytable.Baccarat_paytable(winstate))

        winstate = ""
        winstate +=  BPgame_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
        winstate += BPgame_paytable.combine_winstate(Baccarat_banker_pair,ba_odds_11)
        self.assertEqual([1,1,1,9,12,1],BPgame_paytable.Baccarat_paytable(winstate))


    def test_bigwin_table(self):

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_banker,big_odds_4)
        self.assertEqual([5,5,5],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_player,big_odds_6)
        self.assertEqual([7,7,7],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_player,big_odds_10)
        self.assertEqual([11,11,11],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_banker,big_odds_40)
        self.assertEqual([41,41,41],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_player,big_odds_100)
        self.assertEqual([101,101,101],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_player,big_odds_1000)
        self.assertEqual([1001,1001,1001],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_banker,big_odds_1)
        self.assertEqual([0,2,0],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_player,big_odds_1)
        self.assertEqual([0,0,2],BPgame_paytable.Bigwin_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(bigwin_player,big_odds_0)
        self.assertEqual([0,0,0],BPgame_paytable.Bigwin_paytable(winstate))

    #@unittest.skip("skipping")
    def test_angel_no_wawa_table(self):
        
        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_banker,angel_odds_40)
        self.assertEqual([0,41,0,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_player,angel_odds_40)
        self.assertEqual([0,0,41,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_banker,angel_odds_3)
        self.assertEqual([0,4,0,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_player,angel_odds_3)
        self.assertEqual([0,0,4,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_banker,angel_odds_2)
        self.assertEqual([0,3,0,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_player,angel_odds_2)
        self.assertEqual([0,0,3,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_banker,angel_odds_1)
        self.assertEqual([0,2,0,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_player,angel_odds_1)
        self.assertEqual([0,0,2,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_banker,angel_odds_0)
        self.assertEqual([0,0,0,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_mainbet_player,angel_odds_0)
        self.assertEqual([0,0,0,0,0,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_sidebet_bigangel_banker,angel_odds_2)
        winstate += BPgame_paytable.combine_winstate(angel_sidebet_bigangel_player,angel_odds_2)
        self.assertEqual([0,0,0,3,3,0,0],BPgame_paytable.angel_paytable(winstate))

        winstate = ""
        winstate += BPgame_paytable.combine_winstate(angel_sidebet_perfect_banker,angel_odds_3)
        winstate += BPgame_paytable.combine_winstate(angel_sidebet_perfect_player,angel_odds_3)
        self.assertEqual([0,0,0,0,0,4,4],BPgame_paytable.angel_paytable(winstate))

if __name__ == '__main__':
    unittest.main()
