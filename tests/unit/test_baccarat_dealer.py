import sys
sys.path.append("../..")

import unittest
import baccarat_settle
from player import *
from dealer import *
from BPgame_paytable import *

class DealerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.dealer = dealer(baccarat_settle)
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
                Baccarat_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(1, self.dealer.bet_len(self.player))

        #bet player type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                200,
                Baccarat_player))
        self.assertEqual(200, self.dealer.get_player_bet(self.player))
        self.assertEqual(1, self.dealer.bet_len(self.player))

        #bet banker type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_banker))
        self.assertEqual(300, self.dealer.get_player_bet(self.player))
        self.assertEqual(2, self.dealer.bet_len(self.player))
        
        #bet banker type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                200,
                Baccarat_banker))
        self.assertEqual(400, self.dealer.get_player_bet(self.player))
        self.assertEqual(2, self.dealer.bet_len(self.player))

        #bet banker type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                300,
                Baccarat_banker))
        self.assertEqual(500, self.dealer.get_player_bet(self.player))
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
        self.assertEqual(1, self.dealer.betinfo_len())

        #player2 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player2,
                200,
                1))
        self.assertEqual(200, self.dealer.get_player_bet(self.player2))
        self.assertEqual(2, self.dealer.betinfo_len())
        
        #player3 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player3,
                200,
                1))
        self.assertEqual(200, self.dealer.get_player_bet(self.player3))
        self.assertEqual(3, self.dealer.betinfo_len())

    def test_settle(self):
        print "settle_bet" 

        #win and lost
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            195,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_banker))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            200,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_player))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_banker))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_tie))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(900,
                         self.dealer.get_player_settle(self.player,
                                                       Baccarat_tie))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_banker_pair))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            1200,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_banker_pair))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_player_pair))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            1200,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_player_pair))

        self.dealer.clean_bet()

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_banker_pair))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_player_pair))

        self.dealer.clean_bet()
    def test_tie_withdraw_settle(self):

        #bet banker or player ,win= tie withdraw
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_player))
        self.assertEqual(200, self.dealer.get_player_bet(self.player))

        #settle
        self.assertEqual(
            200,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_tie))

        self.dealer.clean_bet()

        #bet banker|player and tie
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))

        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                Baccarat_tie))
        self.assertEqual(200, self.dealer.get_player_bet(self.player))

        self.assertEqual(
            1000,
            self.dealer.get_player_settle(
                self.player,
                Baccarat_tie))

        self.dealer.clean_bet()


if __name__ == '__main__':
    unittest.main()
