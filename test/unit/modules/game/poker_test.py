#parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,parentdir)

import sys
sys.path.append("../../../../modules/game")

import unittest
from poker import *


class pokerTestCase(unittest.TestCase):

    # prepare work before every test
    def setUp(self):
        self.poker = Poker()
        self.poker.add_slot("playerPoker")
        self.poker.add_slot("BankerPoker")


    # clean work after every test
    def tearDown(self):
        self.poker = None

    def test_remain(self):

        self.poker.shuffle()
        poker = self.poker.deal_cards(1,"playerPoker")
        remain = self.poker.get_remain_cards()
        self.assertEqual(remain, 51)

        poker = self.poker.deal_cards(1,"playerPoker")
        remain = self.poker.get_remain_cards()
        self.assertEqual(remain, 50)

        poker = self.poker.deal_cards(1,"playerPoker")
        remain = self.poker.get_remain_cards()
        self.assertEqual(remain, 49)

    #@unittest.skip("testing skipping")
    def test_card_point(self):

        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s","2_c","3_s","4_s","5_s","6_s","7_s","8_s","9_s","10_d","11_h","12_h","13_h"])

        for i in range(1, 10, 1):
            self.poker.deal_cards(1, "playerPoker")
            self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_POINT), i)
            self.poker.add_slot("playerPoker")

        for i in range(1, 4, 1):
            self.poker.deal_cards(1, "playerPoker")
            self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_POINT), 10)
            self.poker.add_slot("playerPoker")

    #@unittest.skip("testing skipping")
    def test_color_order(self):

        self.poker.color_define(Poker.COLOR_DEF_SHDC)
        self.poker.test_script(["1_s", "2_h", "3_d", "4_c", "5_s", "6_s", "7_s", "8_s", "9_s", "10_d", "11_h", "12_h", "13_h"])

        self.poker.deal_cards(1, "playerPoker")
        poker = self.poker.query("playerPoker", Poker.QUERY_COLOR)
        self.assertEqual(poker, [3])

        self.poker.add_slot("playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        poker = self.poker.query("playerPoker", Poker.QUERY_COLOR)
        self.assertEqual(poker, [2])

        self.poker.add_slot("playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        poker = self.poker.query("playerPoker", Poker.QUERY_COLOR)
        self.assertEqual(poker, [1])

        self.poker.add_slot("playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        poker = self.poker.query("playerPoker", Poker.QUERY_COLOR)
        self.assertEqual(poker, [0])

    #@unittest.skip("testing skipping")
    def test_baccarat_point(self):

        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "2_c", "3_s", "4_s", "5_s", "6_s", "7_s", "8_s", "9_s", "10_d", "11_h", "12_h", "13_h"])

        self.poker.deal_cards(1, "playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_Mod_10_Point), 3)
        self.poker.add_slot("playerPoker")

        self.poker.deal_cards(1, "playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_Mod_10_Point), 7)
        self.poker.add_slot("playerPoker")

        self.poker.deal_cards(1, "playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_Mod_10_Point), 1)
        self.poker.add_slot("playerPoker")

        self.poker.deal_cards(1, "playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_Mod_10_Point), 5)
        self.poker.add_slot("playerPoker")

        self.poker.deal_cards(1, "playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_Mod_10_Point), 9)
        self.poker.add_slot("playerPoker")

        self.poker.deal_cards(1, "playerPoker")
        self.poker.deal_cards(1, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_Mod_10_Point), 0)
        self.poker.add_slot("playerPoker")

    @unittest.skip("testing skipping")
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

    #@unittest.skip("testing skipping")
    def test_check_flush(self):

        self.poker.color_define(Poker.COLOR_DEF_SHDC)
        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "1_c", "2_s", "4_d","5_c"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_FLUSH), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["10_s", "11_s", "12_s", "13_s", "9_s"])

        self.poker.deal_cards(5, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_FLUSH), [3])
        self.poker.add_slot("playerPoker")

    #@unittest.skip("testing skipping")
    def test_check_Pair(self):

        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "2_c", "3_s", "4_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_PAIR), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["1_s", "12_c", "3_s", "12_d"])
        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_PAIR), [12])
        self.poker.add_slot("playerPoker")

    def test_check_twoPair(self):
        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "2_c", "3_s", "4_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_TWO_PAIR), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["10_s", "10_c", "13_s", "13_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_TWO_PAIR), [10,13])
        self.assertEqual(len(self.poker.query("playerPoker", Poker.QUERY_TWO_PAIR)), 2)
        self.poker.add_slot("playerPoker")

    def test_check_tripple(self):
        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "1_c", "2_s", "4_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_TRIPPLE), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["10_s", "10_c", "13_s", "10_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_TRIPPLE), [10])
        self.assertEqual(len(self.poker.query("playerPoker", Poker.QUERY_TRIPPLE)), 1)
        self.poker.add_slot("playerPoker")

    def test_check_straight(self):
        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "1_c", "2_s", "4_d","5_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_STRAIGHT), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["9_s", "10_c", "11_s", "12_d","13_d"])

        self.poker.deal_cards(5, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_STRAIGHT), [9,10,11,12,13])
        self.poker.add_slot("playerPoker")

        #multi count will be miss judet
        # self.poker.test_script(["9_s", "10_c", "11_d", "12_d", "13_d","8_d"])
        #
        # self.poker.deal_cards(6, "playerPoker")
        # self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_STRAIGHT), [])
        # self.poker.add_slot("playerPoker")

    def test_check_fullhouse(self):
        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "1_c", "2_s", "4_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_FULLHOUSE), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["10_s", "10_c", "13_s","10_d","13_d"])

        self.poker.deal_cards(5, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_FULLHOUSE), [[13],[10]])
        self.poker.add_slot("playerPoker")

    def test_check_four_of_a_kind(self):
        self.poker.point_define(Poker.POINT_DEF_BACCART)
        self.poker.test_script(["1_s", "1_c", "2_s", "4_d"])

        self.poker.deal_cards(4, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_FOUR_OF_A_KIND), [])
        self.poker.add_slot("playerPoker")

        self.poker.test_script(["10_s", "10_c", "13_s","10_d","10_h"])

        self.poker.deal_cards(5, "playerPoker")
        self.assertEqual(self.poker.query("playerPoker", Poker.QUERY_FOUR_OF_A_KIND), [10])
        self.poker.add_slot("playerPoker")

    #POKER_ROYAL_FLUSH
    #POKER_STRAIGHT_FLUSH
    #POKER_ROYAL_FLUSH

    @unittest.skip("testing skipping")
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

    @unittest.skip("testing skipping")
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

    @unittest.skip("testing skipping")
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


if __name__ == '__main__':
    unittest.main()
