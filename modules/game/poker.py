import random
import itertools
from collections import Counter

class Poker(object):
    def __init__(self):
        self._dealed_cards = 0
        self._test_data = None
        self._cards = ["1c", "1d", "1h", "1s", "2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s",
           "4c", "4d", "4h", "4s", "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s",
           "7c", "7d", "7h", "7s", "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s",
           "ic", "id", "ih", "is", "jc", "jd", "jh", "js", "qc", "qd", "qh", "qs",
           "kc", "kd", "kh", "ks"]


    def shuffle(self):
        random.shuffle(self._cards)
        self._dealed_cards = 0

    def deal_cards(self, numbers):

        if self._test_data != None:
           card = self._test_data[0:1]
           self._test_data.pop(0)
           return card

        if (numbers + self._dealed_cards) <= len(self._cards):
            start = self._dealed_cards
            end = self._dealed_cards + numbers
            self._dealed_cards += numbers
            return self._cards[start:end]
        else:
            return None

    def get_remain_cards(self):
        remain = len(self._cards) - self._dealed_cards
        return remain

    def test_script(self,test_data):
        self._test_data = test_data


class PokerPoint(object):
    #showhand type
    POKER_ROYAL_FLUSH =       11
    POKER_STRAIGHT_FLUSH =    10
    POKER_FOUR_OF_A_KIND =    9
    POKER_FULL_HOUSE =        8
    POKER_FLUSH =             7
    POKER_BIG_STRAIGHT =      6
    POKER_STRAIGHT =          5
    POKER_TRIPPLE =           4
    POKER_TWO_PAIR =          3
    POKER_ONE_PAIR_BIG =      2
    POKER_ONE_PAIR_NORMAL =   1
    POKER_NONE =              0
    #color type
    COLOR_SPADE =             0
    COLOR_HEART =             1 
    COLOR_DIAMOND =           2
    COLOR_CLUB =              3

    NEWNEW_CARD_NUM =         5

    POKER_TRUE =              1
    POKER_FALSE =             0
    POKER_ERRROR =           -1

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
        temp = [0]*5
        for i in range(5):
             temp[i] = PokerPoint.get_card_point(card[i])

        temp.sort()
        if (temp[4]-temp[3]) == 1 and (temp[3]-temp[2]) ==1 and (temp[2]-temp[1]) == 1:
            if(temp[0] == 1) and (temp[4] == 13):
                 return PokerPoint.POKER_BIG_STRAIGHT
            elif (temp[1] - temp[0]) == 1:
                return PokerPoint.POKER_STRAIGHT
        
        return PokerPoint.POKER_NONE

    @staticmethod
    def check_flush(card):
        colors = [0]*5
        for i in range(5):
            colors[i] = PokerPoint.get_card_color(card[i])
    
        items = Counter(colors)

        if len(items) > 1:
            return PokerPoint.POKER_NONE
        else:
            return PokerPoint.POKER_FLUSH
    @staticmethod
    def check_pair_type(cards):
        
        temp = [0]*5
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
                    if key==1 or key == 10 or key==11 or key==12 or key==13:
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
    def check_baccarat_player_extra_card_rule(poker):
        point = PokerPoint.get_baccarat_point(poker)
        return PokerPoint.baccarat_player_extra_card_rule(point)

    @staticmethod
    def check_baccarat_top_card_rule(poker):
        point = PokerPoint.get_baccarat_point(poker)
        if point >=8:
            return True 
        return False

    @staticmethod
    def baccarat_player_extra_card_rule(point):
        if point >= 6:
            return False
        return True

    @staticmethod
    def check_baccarat_banker_extra_card_rule(player_poker,banker_poker):
        banker_point = PokerPoint.get_baccarat_point(banker_poker)
        player_third_point = PokerPoint.get_baccarat_point(player_poker[-1:])

        if banker_point <= 2:
            return True

        if banker_point == 3:
            if player_third_point ==8:
                return False
            else:
                return True

        if banker_point == 4:
            if player_third_point == 0 or player_third_point ==1 or player_third_point == 8 or player_third_point == 9:
                return False
            else:
                return True

        if banker_point == 5:
            if player_third_point == 0 or player_third_point == 1 or player_third_point == 2 or player_third_point == 3 or player_third_point == 8 or player_third_point == 9:
                return False
            else:
                return True

        if banker_point == 6:
            if len(player_poker) != 3:
                return False
            else:
                if player_third_point == 6 or player_third_point == 7:
                    return True
                else:
                    return False

        return False

    @staticmethod
    def check_newnew_five_wawa(cards):
        map_cards = map(lambda x:PokerPoint.get_card_point(x), cards)
        #print map_cards
        if min(map_cards) >= 11:
            return max(map_cards)
        else:
            return 0

    @staticmethod
    def check_newnew_four_of_a_kind(cards):
        temp = [0]*5
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
        total_comb_point = [0]*len(back_cards_comb)

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
        #return max(map(lambda x:PokerPoint.POKER_ORDER.index(x), cards))
        map_cards = map(lambda x:PokerPoint.POKER_ORDER.index(x), cards)
        max_cards_order = max(map_cards)
        #print map_cards, max_cards_order
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

