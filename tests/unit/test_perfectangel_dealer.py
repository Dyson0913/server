import sys
sys.path.append("../..")

import unittest
import perfectangel_settle
from player import *
from dealer import *
from BPgame_paytable import *

class DealerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.dealer = dealer(perfectangel_settle)
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

        #bet banker type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                angel_bet_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))
        self.assertEqual(1, self.dealer.bet_len(self.player))

        #bet banker type
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                200,
                angel_bet_banker))
        self.assertEqual(200, self.dealer.get_player_bet(self.player))
        self.assertEqual(1, self.dealer.bet_len(self.player))

        #settle
        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                angel_player_normal_win))

    def test_multi_player_bet(self):

        #player1 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                angel_bet_banker))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))

        #player2 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player2,
                200,
                angel_bet_banker))
        self.assertEqual(200, self.dealer.get_player_bet(self.player2))

        #player3 bet
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player3,
                200,
                angel_bet_banker))
        self.assertEqual(200, self.dealer.get_player_bet(self.player3))

    def test_settle(self):
 
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                angel_bet_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))

        #five wawa win
        self.assertEqual(
            4000,
            self.dealer.get_player_settle(
                self.player,
                angel_player_five_wawa_win))

        #four of a kind win
        self.assertEqual(
            4000,
            self.dealer.get_player_settle(
                self.player,
                angel_player_four_of_a_kind_win))
 
        #newnew win
        self.assertEqual(
            300,
            self.dealer.get_player_settle(
                self.player,
                angel_player_newnew_win))

        #normal win
        self.assertEqual(
            200,
            self.dealer.get_player_settle(
                self.player,
                angel_player_normal_win))
        
        self.dealer.clean_bet()

        #lost
        self.assertTrue(
            True,
            self.dealer.new_bet(
                self.player,
                100,
                angel_bet_player))
        self.assertEqual(100, self.dealer.get_player_bet(self.player))

        #all kind of lost
        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                angel_banker_five_wawa_win))
        
        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                angel_banker_four_of_a_kind_win))

        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                angel_banker_newnew_win))

        self.assertEqual(
            0,
            self.dealer.get_player_settle(
                self.player,
                angel_banker_normal_win))


if __name__ == '__main__':
    unittest.main()
