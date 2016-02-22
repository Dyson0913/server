#import os,sys
#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,parentdir)

import sys
sys.path.append("../..")

import unittest
from poker import *


class pokerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.poker = Poker()

    # clean work after every test
    def tearDown(self):
        self.poker = None

    def test_remain(self):

        self.poker.shuffle()
        poker = self.poker.deal_cards(0)
        remain = self.poker.get_remain_cards()
        self.assertEqual(remain, 52)

        poker = self.poker.deal_cards(52)
        remain = self.poker.get_remain_cards()
        self.assertEqual(remain, 0)

        poker = self.poker.deal_cards(53)
        remain = self.poker.get_remain_cards()
        self.assertEqual(remain, 0)

    def test_get_card_point(self):
        for i in range(1, 9, 1):
            poker = (str(i) + "d")
            point = PokerPoint.get_card_point(poker)
            self.assertEqual(point, i)

        poker = ("id")
        point = PokerPoint.get_card_point(poker)
        self.assertEqual(point, 10)

        poker = ("jd")
        point = PokerPoint.get_card_point(poker)
        self.assertEqual(point, 11)

        poker = ("qd")
        point = PokerPoint.get_card_point(poker)
        self.assertEqual(point, 12)

        poker = ("kd")
        point = PokerPoint.get_card_point(poker)
        self.assertEqual(point, 13)

    def test_get_baccarat_point(self):
        for i in range(1, 9, 1):
            poker = (str(i) + "d")
            point = PokerPoint.get_baccarat_card_point(poker)
            self.assertEqual(point, i)

        poker = ("id")
        point = PokerPoint.get_baccarat_card_point(poker)
        self.assertEqual(point, 10)

        poker = ("jd")
        point = PokerPoint.get_baccarat_card_point(poker)
        self.assertEqual(point, 10)

        poker = ("qd")
        point = PokerPoint.get_baccarat_card_point(poker)
        self.assertEqual(point, 10)

        poker = ("kd")
        point = PokerPoint.get_baccarat_card_point(poker)
        self.assertEqual(point, 10)

    def test_card_color(self):

        poker = ("1s")
        point = PokerPoint.get_card_color(poker)
        self.assertEqual(point, PokerPoint.COLOR_SPADE)

        poker = ("2h")
        point = PokerPoint.get_card_color(poker)
        self.assertEqual(point, PokerPoint.COLOR_HEART)

        poker = ("3d")
        point = PokerPoint.get_card_color(poker)
        self.assertEqual(point, PokerPoint.COLOR_DIAMOND)

        poker = ("4c")
        point = PokerPoint.get_card_color(poker)
        self.assertEqual(point, PokerPoint.COLOR_CLUB)

    def test_baccarat_point(self):

        poker = []
        point = PokerPoint.get_baccarat_point(poker)
        self.assertEqual(point, 0)

        poker = ["is", "js", "qs", "ks"]
        point = PokerPoint.get_baccarat_point(poker)
        self.assertEqual(point, 0)

        poker = ["1s", "2s"]
        point = PokerPoint.get_baccarat_point(poker)
        self.assertEqual(point, 3)

        poker = ["8s", "9s"]
        point = PokerPoint.get_baccarat_point(poker)
        self.assertEqual(point, 7)

        poker = ["8s", "is"]
        point = PokerPoint.get_baccarat_point(poker)
        self.assertEqual(point, 8)

    def test_check_straight(self):

        poker = ["9s", "is", "js", "qs", "ks"]
        point = PokerPoint.check_straight(poker)
        self.assertEqual(point, PokerPoint.POKER_STRAIGHT)

        poker = ["is", "js", "qs", "ks", "1s"]
        point = PokerPoint.check_straight(poker)
        self.assertEqual(point, PokerPoint.POKER_BIG_STRAIGHT)

        poker = ["3s", "is", "js", "qs", "ks"]
        point = PokerPoint.check_straight(poker)
        self.assertEqual(point, PokerPoint.POKER_NONE)

    def test_check_flush(self):

        poker = ["9s", "is", "js", "qs", "ks"]
        point = PokerPoint.check_flush(poker)
        self.assertEqual(point, PokerPoint.POKER_FLUSH)

        poker = ["id", "js", "qs", "ks", "1s"]
        point = PokerPoint.check_flush(poker)
        self.assertEqual(point, PokerPoint.POKER_NONE)

    def test_check_Pair_type(self):

        poker = ["9s", "8c", "2h", "7d", "is"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_NONE)

        poker = ["9s", "ic", "ih", "id", "is"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_FOUR_OF_A_KIND)

        poker = ["2d", "2s", "2h", "5s", "5d"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_FULL_HOUSE)

        poker = ["2d", "2s", "2h", "1s", "5d"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_TRIPPLE)

        poker = ["2d", "2s", "4h", "4s", "5d"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_TWO_PAIR)

        poker = ["id", "is", "2h", "1s", "5d"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_ONE_PAIR_BIG)

        poker = ["2d", "7s", "2h", "1s", "5d"]
        point = PokerPoint.check_pair_type(poker)
        self.assertEqual(point, PokerPoint.POKER_ONE_PAIR_NORMAL)

    def test_check_big_win_show_hand(self):

        poker = ["id", "jd", "qd", "kd", "1d"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_ROYAL_FLUSH)

        poker = ["5d", "6d", "7d", "8d", "9d"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_STRAIGHT_FLUSH)

        poker = ["5d", "6d", "7h", "8s", "9s"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_STRAIGHT)

        poker = ["5s", "6s", "7s", "8s", "is"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_FLUSH)

        poker = ["5d", "5s", "5h", "5c", "9d"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_FOUR_OF_A_KIND)

        poker = ["5d", "5s", "5h", "6c", "6d"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_FULL_HOUSE)

        poker = ["5d", "5d", "6h", "6s", "9d"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_NONE)

        poker = ["5d", "5s", "7h", "1c", "9d"]
        point = PokerPoint.check_big_win_show_hand(poker)
        self.assertEqual(point, PokerPoint.POKER_NONE)

    def test_get_newnew_point(self):

        poker = ["7c", "8h", "qs", "1s", "5c"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 1)

        poker = ["3c", "4d", "kh", "kc", "5h"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 0)

        poker = ["2h", "5d", "jc", "id", "3s"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 10)

        poker = ["3c", "4c", "3h", "jc", "kh"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 10)

        poker = ["id", "8c", "6h", "qh", "5s"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 0)

        poker = ["3s", "is", "7s", "1s", "8d"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 9)

        poker = ["9h", "3d", "8s", "6h", "8c"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 4)

        poker = ["4c", "2h", "4s", "qd", "qh"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 10)

        poker = ["jc", "qh", "ks", "2d", "qh"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 2)

        poker = ["jc", "qh", "ks", "1d", "qh"]
        point = PokerPoint.get_newnew_point(poker)
        self.assertEqual(point, 1)

    def test_bacc_player_extra_rule(self):

        expected = True

        for i in range(1, 5, 1):
            new = (str(i) + "d")
            poker = [new, "ks"]
            result = PokerPoint.check_baccarat_player_extra_card_rule(poker)
            self.assertTrue(expected, result)

        poker = ["is", "ks"]
        result = PokerPoint.check_baccarat_player_extra_card_rule(poker)
        self.assertTrue(expected, result)

        expected = False
        poker = ["6s", "ks"]
        result = PokerPoint.check_baccarat_player_extra_card_rule(poker)
        self.assertFalse(expected, result)

        poker = ["7s", "ks"]
        result = PokerPoint.check_baccarat_player_extra_card_rule(poker)
        self.assertFalse(expected, result)

        poker = ["8s", "ks"]
        result = PokerPoint.check_baccarat_player_extra_card_rule(poker)
        self.assertFalse(expected, result)

        poker = ["9s", "ks"]
        result = PokerPoint.check_baccarat_player_extra_card_rule(poker)
        self.assertFalse(expected, result)

    def test_bacc_banker_extra_rule(self):

        # 1,2 point
        expected = True
        for i in range(1,3):
            new = [str(i)+"d"]
            result = PokerPoint.check_baccarat_banker_extra_card_rule(new, new)
            self.assertTrue(expected, result)
        
        # 0 point rule
        new = ["id","is"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(new, new)
        self.assertTrue(expected, result)

        # 3 point rule
        expected = True
        for i in range(1,10):
            player = [str(i) + "d"]
            banker = ["3s", "ks"]
            result = PokerPoint.check_baccarat_banker_extra_card_rule(
                player,
                banker)
            if i == 8:
                self.assertFalse(False, result)
            else:
                self.assertTrue(expected, result)

        player = ["id"]
        banker = ["3s", "ks"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertTrue(expected, result)

        # 4 point rule
        expected = True
        for i in range(1,10):
            player = [str(i) + "d"]
            banker = ["4s", "ks"]
            result = PokerPoint.check_baccarat_banker_extra_card_rule(
                player,
                banker)
            if i == 1 or i == 8 or i == 9:
                self.assertFalse(False, result)
            else:
                self.assertTrue(expected, result)

        player = ["id"]
        banker = ["4s", "ks"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertFalse(False, result)

        # 5 point rule
        expected = True
        for i in range(1,10):
            player = [str(i) + "d"]
            banker = ["5s", "ks"]
            result = PokerPoint.check_baccarat_banker_extra_card_rule(
                player,
                banker)
            if i == 1 or i == 2 or i == 3 or i == 8 or i == 9:
                self.assertFalse(False, result)
            else:
                self.assertTrue(expected, result)

        player = ["id"]
        banker = ["5s", "ks"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertFalse(False, result)

        # 6 point rule
        expected = True
        for i in range(1,10):
            #player 3 card judet
            player = ["is","qs",str(i) + "d"]
            banker = ["6s", "ks"]
            result = PokerPoint.check_baccarat_banker_extra_card_rule(
                player,
                banker)
            if i == 6 or i == 7:
                self.assertTrue(expected, result)
            else:
                self.assertFalse(False, result)
            #player 2 card  reject
            player = ["is",str(i) + "d"]
            banker = ["6s", "ks"]
            result = PokerPoint.check_baccarat_banker_extra_card_rule(
                player,
                banker)
            if i == 6 or i == 7:
                self.assertTrue(expected, result)
            else:
                self.assertFalse(False, result)

        player = ["id"]
        banker = ["6s", "ks"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertFalse(False, result)

        # 7 point rule
        player = ["jh"]
        banker = ["is", "7s"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertFalse(False, result)

        # 8 point rule
        player = ["8d"]
        banker = ["8s", "ks"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertFalse(False, result)

        # 9 point rule
        player = ["9d"]
        banker = ["9s", "ks"]
        result = PokerPoint.check_baccarat_banker_extra_card_rule(
            player,
            banker)
        self.assertFalse(False, result)


    def test_bacc_top_card_rule(self):

        #0 1
        new = ["9d","1s"]
        result = PokerPoint.check_baccarat_top_card_rule(new)
        self.assertEqual(False, result)

        new = ["id","1s"]
        result = PokerPoint.check_baccarat_top_card_rule(new)
        self.assertEqual(False, result)

        #2~7
        for i in range(1,7):
            new = [(str(i) + "d"),"1s"]
            result = PokerPoint.check_baccarat_top_card_rule(new)
            self.assertEqual(False, result)

        #8 9
        new = ["7d","1s"]
        result = PokerPoint.check_baccarat_top_card_rule(new)
        self.assertEqual(True, result)

        new = ["8d","1s"]
        result = PokerPoint.check_baccarat_top_card_rule(new)
        self.assertEqual(True, result)

    def test_front_end_point(self):
        poker = ["is","jh","qd","kc"]
        point = PokerPoint.get_db_mapping(poker)
        self.assertEqual(point, "STHJDQCK")

        poker = ["1s","2h","3d","4c","5c","6d","7s","8d","9s"]
        point = PokerPoint.get_db_mapping(poker)
        self.assertEqual(point, "S1H2D3C4C5D6S7D8S9")

    def test_cards_max_order(self):

        poker = ["1d","9d","id", "jd", "qd", "kd"]
        point = PokerPoint.get_cards_max_order(poker)
 

if __name__ == '__main__':
    unittest.main()
