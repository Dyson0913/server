import sys
sys.path.append("../..")

import unittest
import bigwin_settle
from player import *
from dealer import *
from BPgame_paytable import *


class DealerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.dealer = dealer(bigwin_settle)
        self.player = PlayerInfo()
        self.player2 = PlayerInfo()
        self.player3 = PlayerInfo()

    # clean work after every test
    def tearDown(self):
        self.dealer = None
        self.player = None
        self.player2 = None
        self.player3 = None

    def test_bet(self):

        #bet player type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(1, self.dealer.bet_len(self.player))

        #bet banker type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                200,
                bigwin_banker))
        self.assertEqual(300, self.dealer.get_player_bet(self.player))
        self.assertEqual(2, self.dealer.bet_len(self.player))
        
        #bet player type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                200,
                bigwin_player))

        self.assertEqual(400, self.dealer.get_player_bet(self.player))
        self.assertEqual(2, self.dealer.bet_len(self.player))

    def test_multi_player_bet(self):

        print "multi_player_bet"

        #player1 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                1))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))

        #player2 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player2,
                200,
                1))
        self.assertEqual(200, self.dealer.get_player_bet(self.player2))
        
        #player3 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player3,
                200,
                1))
        self.assertEqual(200, self.dealer.get_player_bet(self.player3))

    def test_settle(self):

        #win and lost
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            200,
            self.dealer.get_player_settle(
                self.player,
                bigwin_banker))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            200,
            self.dealer.get_player_settle(
                self.player,
                bigwin_player))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(0,
                         self.dealer.get_player_settle(self.player,
                                                       bigwin_banker))

    def test_settle_special_type(self):

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            100100,
            self.dealer.get_player_settle(
                self.player,
                PokerPoint.POKER_ROYAL_FLUSH))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            10100,
            self.dealer.get_player_settle(
                self.player,
                PokerPoint.POKER_STRAIGHT_FLUSH))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            4100,
            self.dealer.get_player_settle(
                self.player,
                PokerPoint.POKER_FOUR_OF_A_KIND))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            1100,
            self.dealer.get_player_settle(
                self.player,
                PokerPoint.POKER_FULL_HOUSE))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            700,
            self.dealer.get_player_settle(
                self.player,
                PokerPoint.POKER_FLUSH))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            500,
            self.dealer.get_player_settle(
                self.player,
                PokerPoint.POKER_STRAIGHT))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                bigwin_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(0,
                         self.dealer.get_player_settle(self.player,
                                                       bigwin_allkill))

if __name__ == '__main__':
    unittest.main()
