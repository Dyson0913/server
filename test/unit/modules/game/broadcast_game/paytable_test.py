import sys
sys.path.append("../../../../../modules/game")
sys.path.append("../../../../../modules/game/broadcast_game")

import unittest
from poker import *
import ba_paytable
from ba_paytable import *

class DealerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        pass

    # clean work after every test
    def tearDown(self):
        pass

    def test_baccarat_table(self):
        winstate = ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        self.assertEqual([0,1.95,0,0,0,0],ba_paytable.paytable(winstate))

        winstate = ""
        winstate += ba_paytable.combine_winstate(Baccarat_player,ba_odds_1)
        self.assertEqual([0,0,2,0,0,0],ba_paytable.paytable(winstate))

        winstate = ""
        winstate +=  ba_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
        self.assertEqual([1,1,1,9,1,1],ba_paytable.paytable(winstate))

        #multi winstate
        winstate = ""
        winstate = ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        winstate +=  ba_paytable.combine_winstate(Baccarat_banker_pair,ba_odds_11)
        self.assertEqual([0,1.95,0,0,12,0],ba_paytable.paytable(winstate))

        winstate = ""
        winstate += ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        winstate += ba_paytable.combine_winstate(Baccarat_banker_pair,ba_odds_11)
        winstate += ba_paytable.combine_winstate(Baccarat_player_pair,ba_odds_11)
        self.assertEqual([0,1.95,0,0,12,12],ba_paytable.paytable(winstate))

        winstate = ""
        winstate +=  ba_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
        winstate += ba_paytable.combine_winstate(Baccarat_banker_pair,ba_odds_11)
        self.assertEqual([1,1,1,9,12,1],ba_paytable.paytable(winstate))


    #@unittest.skip("skipping")

if __name__ == '__main__':
    unittest.main()
