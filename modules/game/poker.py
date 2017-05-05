import random
import itertools
from pylog import *
from collections import Counter

class Poker(object):

    QUERY_AMOUNT = "len"
    QUERY_POINT = "point"
    QUERY_Mod_10_Point = "Modpoint"
    QUERY_POKER = "poker"

    POINT_DEF_BACCART = "baccart"

    def __init__(self):
        self._dealed_cards = 0
        self._dataslot = {}
        self._point_def =[]
        self._test_data = None
        self._cards = ["1_c", "1_d", "1_h", "1_s", "2_c", "2_d", "2_h", "2_s", "3_c", "3_d", "3_h", "3_s",
                       "4_c", "4_d", "4_h", "4_s", "5_c", "5_d", "5_h", "5_s", "6_c", "6_d", "6_h", "6_s",
                       "7_c", "7_d", "7_h", "7_s", "8_c", "8_d", "8_h", "8_s", "9_c", "9_d", "9_h", "9_s",
                       "10_c", "10_d", "10_h", "10_s", "11_c", "11_d", "11_h", "11_s", "12_c", "12_d", "12_h", "12_s",
                       "13_c", "13_d", "13_h", "13_s"]

    def add_slot(self, slotname):
        self._dataslot.update({slotname: None})

    def point_define(self,def_type):

        if def_type == self.POINT_DEF_BACCART:
            self._point_def = [0,1,2,3,4,5,6,7,8,9,10,10,10,10]

    def shuffle(self):
        random.shuffle(self._cards)
        self._dealed_cards = 0

    def deal_cards(self, numbers, slotname):

        if self._test_data != None:
            card = self._test_data[0:1]
            self._test_data.pop(0)
            poker = self._dataslot[slotname]
            if poker == None:
                self._dataslot[slotname] = card
                logging.info(slotname + " card " + str(self._dataslot[slotname]))
                return
            else:
                poker.extend(card)
                self._dataslot[slotname] = poker
                logging.info(slotname + " card " + str(self._dataslot[slotname]))
                return

        if (numbers + self._dealed_cards) <= len(self._cards):
            start = self._dealed_cards
            end = self._dealed_cards + numbers
            self._dealed_cards += numbers
            poker = self._dataslot[slotname]
            if poker == None:
                self._dataslot[slotname] = self._cards[start:end]
            else:
                poker.extend(self._cards[start:end])
                self._dataslot[slotname] = poker

        logging.info(slotname +" card "+str(self._dataslot[slotname]))

    def query(self,slotname,querytype):

        if querytype == self.QUERY_AMOUNT:
            poker = self._dataslot[slotname]
            if poker == None:
                return 0
            else:
                return len(poker)

        if querytype == self.QUERY_POINT:
            poker = self._dataslot[slotname]
            if poker == None:
                return -1
            else:
                point_list = map(lambda x:self._point_def[int(x.split("_")[0])], poker)
                point = reduce(lambda x,y: x+y, point_list)
                return point

        if querytype == self.QUERY_Mod_10_Point:
            return self.query(slotname,self.QUERY_POINT) % 10

        if querytype == self.QUERY_POKER:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                return poker

    def copy_To(self, slotname,data ):
        self._dataslot[slotname] = data

    def get_remain_cards(self):
        remain = len(self._cards) - self._dealed_cards
        return remain

    def test_script(self, test_data):
        self._test_data = test_data


class PokerPoint(object):
    # showhand type
    POKER_ROYAL_FLUSH = 11
    POKER_STRAIGHT_FLUSH = 10
    POKER_FOUR_OF_A_KIND = 9
    POKER_FULL_HOUSE = 8
    POKER_FLUSH = 7
    POKER_BIG_STRAIGHT = 6
    POKER_STRAIGHT = 5
    POKER_TRIPPLE = 4
    POKER_TWO_PAIR = 3
    POKER_ONE_PAIR_BIG = 2
    POKER_ONE_PAIR_NORMAL = 1
    POKER_NONE = 0
    # color type
    COLOR_SPADE = 0
    COLOR_HEART = 1
    COLOR_DIAMOND = 2
    COLOR_CLUB = 3

    NEWNEW_CARD_NUM = 5

    POKER_TRUE = 1
    POKER_FALSE = 0
    POKER_ERRROR = -1

    POKER_ORDER = ["1c", "1d", "1h", "1s", "2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s",
                   "4c", "4d", "4h", "4s", "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s",
                   "7c", "7d", "7h", "7s", "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s",
                   "ic", "id", "ih", "is", "jc", "jd", "jh", "js", "qc", "qd", "qh", "qs",
                   "kc", "kd", "kh", "ks"]

    @staticmethod
    def get_card_point(card):
        l = list(card)
        if (card[0] == "i"):
            point = 10
        elif (card[0] == "j"):
            point = 11
        elif (card[0] == "q"):
            point = 12
        elif (card[0] == "k"):
            point = 13
        else:
            point = int(card[0])
        return point

    @staticmethod
    def get_baccarat_card_point(card):
        l = list(card)
        if (card[0] == "i" or card[0] == "j" or card[0] == "q" or card[0] == "k"):
            point = 10
        else:
            point = int(card[0])

        return point

    @staticmethod
    def get_card_color(card):
        l = list(card)
        if (card[1] == "s"):
            return PokerPoint.COLOR_SPADE
        elif (card[1] == "h"):
            return PokerPoint.COLOR_HEART
        elif (card[1] == "d"):
            return PokerPoint.COLOR_DIAMOND
        else:
            return PokerPoint.COLOR_CLUB

    @staticmethod
    def get_baccarat_point(cards):
        point = 0
        for card in cards:
            card_point = PokerPoint.get_baccarat_card_point(card)
            point += card_point

        point = point % 10

        return point

    @staticmethod
    def check_straight(card):
        temp = [0] * 5
        for i in range(5):
            temp[i] = PokerPoint.get_card_point(card[i])

        temp.sort()
        if (temp[4] - temp[3]) == 1 and (temp[3] - temp[2]) == 1 and (temp[2] - temp[1]) == 1:
            if (temp[0] == 1) and (temp[4] == 13):
                return PokerPoint.POKER_BIG_STRAIGHT
            elif (temp[1] - temp[0]) == 1:
                return PokerPoint.POKER_STRAIGHT

        return PokerPoint.POKER_NONE

    @staticmethod
    def check_flush(card):
        colors = [0] * 5
        for i in range(5):
            colors[i] = PokerPoint.get_card_color(card[i])

        items = Counter(colors)

        if len(items) > 1:
            return PokerPoint.POKER_NONE
        else:
            return PokerPoint.POKER_FLUSH

    @staticmethod
    def check_pair_type(cards):

        temp = [0] * 5
        for i in range(5):
            temp[i] = PokerPoint.get_card_point(cards[i])

        c = Counter(temp)
        if len(c) == 2:
            key, value = c.popitem()
            if value == 1 or value == 4:
                return PokerPoint.POKER_FOUR_OF_A_KIND
            else:
                return PokerPoint.POKER_FULL_HOUSE
        elif len(c) == 3:
            for i in range(len(c)):
                key, value = c.popitem()
                if value == 3:
                    return PokerPoint.POKER_TRIPPLE
                if value == 2:
                    return PokerPoint.POKER_TWO_PAIR
        elif len(c) == 4:
            for i in range(len(c)):
                key, value = c.popitem()
                if value == 2:
                    if key == 1 or key == 10 or key == 11 or key == 12 or key == 13:
                        return PokerPoint.POKER_ONE_PAIR_BIG
                    else:
                        return PokerPoint.POKER_ONE_PAIR_NORMAL

        return PokerPoint.POKER_NONE

    @staticmethod
    def check_show_hand(cards):
        is_straight = PokerPoint.check_straight(cards)

        if is_straight != PokerPoint.POKER_NONE:
            if PokerPoint.check_flush(cards) == PokerPoint.POKER_FLUSH:
                if is_straight == PokerPoint.POKER_BIG_STRAIGHT:
                    return PokerPoint.POKER_ROYAL_FLUSH
                else:
                    return PokerPoint.POKER_STRAIGHT_FLUSH
            else:
                return PokerPoint.POKER_STRAIGHT
        elif PokerPoint.check_flush(cards) == PokerPoint.POKER_FLUSH:
            return PokerPoint.POKER_FLUSH
        else:
            value = PokerPoint.check_pair_type(cards)
            return value

    @staticmethod
    def check_newnew_five_wawa(cards):
        map_cards = map(lambda x: PokerPoint.get_card_point(x), cards)
        # print map_cards
        if min(map_cards) >= 11:
            return max(map_cards)
        else:
            return 0

    @staticmethod
    def check_newnew_four_of_a_kind(cards):
        temp = [0] * 5
        for i in range(5):
            temp[i] = PokerPoint.get_card_point(cards[i])

        c = Counter(temp)
        if len(c) == 2:
            for i in range(2):
                key, value = c.popitem()
                if value == 4:
                    return key
        else:
            return 0

    @staticmethod
    def get_newnew_point(cards):

        if (len(cards) != PokerPoint.NEWNEW_CARD_NUM):
            return PokerPoint.POKER_ERROR

        back_cards_comb = list(itertools.combinations(cards, 3))

        back_cards_point = 0
        total_comb_point = [0] * len(back_cards_comb)

        for i in range(len(back_cards_comb)):
            back_cards_point = PokerPoint.get_baccarat_point(back_cards_comb[i])

            if back_cards_point == 0:
                two_cards = list(set(cards) - set(back_cards_comb[i]))
                two_cards_point = PokerPoint.get_baccarat_point(two_cards)
                if two_cards_point == 0:
                    two_cards_point = 10
                total_comb_point[i] = two_cards_point
            else:
                total_comb_point[i] = 0

        final_point = max(total_comb_point)

        return final_point

    @staticmethod
    def get_cards_max_order(cards):
        # return max(map(lambda x:PokerPoint.POKER_ORDER.index(x), cards))
        map_cards = map(lambda x: PokerPoint.POKER_ORDER.index(x), cards)
        max_cards_order = max(map_cards)
        # print map_cards, max_cards_order
        return max_cards_order

    @staticmethod
    def compare_cards_order(cards1, cards2):

        if len(cards1) != len(cards2):
            return PokerPoint.POKER_ERROR

        max_cards1_order = PokerPoint.get_cards_max_order(cards1)
        max_cards2_order = PokerPoint.get_cards_max_order(cards2)

        if max_cards1_order > max_cards2_order:
            return PokerPoint.POKER_TRUE
        elif max_cards2_order > max_cards1_order:
            return PokerPoint.POKER_FALSE
        else:
            return PokerPoint.POKER_ERROR

