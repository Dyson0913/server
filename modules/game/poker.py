import random
import itertools
from pylog import *
from collections import Counter

class Poker(object):

    #query attribute
    QUERY_AMOUNT = "len"
    QUERY_POINT = "point"
    QUERY_Mod_10_Point = "Modpoint"
    QUERY_POKER = "poker"
    QUERY_COLOR = "color"
    QUERY_DEF_POINT_ARR = "def_point_Arr"
    QUERY_POINT_ARR = "pointArr"

    QUERY_PAIR = "pair"
    QUERY_TWO_PAIR = "twopair"
    QUERY_TRIPPLE = "tripple"
    QUERY_STRAIGHT = "straight"
    QUERY_FLUSH = "flush"
    QUERY_FULLHOUSE = "fullhouse"
    QUERY_FOUR_OF_A_KIND = "fourofakind"

    #point define
    POINT_DEF_BACCART = "baccart"

    #color define
    COLOR_DEF_SHDC = "SHDC"

    def __init__(self):
        self._dealed_cards = 0
        self._dataslot = {}
        self._point_def =[]
        self._color_def = []
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

    def color_define(self,def_type):

        if def_type == self.COLOR_DEF_SHDC:
            #s biggiest 0,1,2,3
            self._color_def = ["c","d","h","s"]

    def shuffle(self):
        random.shuffle(self._cards)
        self._dealed_cards = 0

    def deal_cards(self, numbers, slotname):

        if self._test_data != None:
            card = self._test_data[0:numbers]
            self._test_data.pop(0)
            poker = self._dataslot[slotname]
            if poker == None:
                self._dataslot[slotname] = card
                return
            else:
                poker.extend(card)
                self._dataslot[slotname] = poker
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

        if querytype == self.QUERY_COLOR:
            poker = self._dataslot[slotname]
            if poker == None:
                return None
            else:
                color_list = map(lambda x: self._color_def.index(x.split("_")[1]), poker)
                return color_list

        if querytype == self.QUERY_DEF_POINT_ARR:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                point_list = map(lambda x: self._point_def[int(x.split("_")[0])], poker)
                return point_list

        if querytype == self.QUERY_POINT_ARR:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                point_list = map(lambda x: int(x.split("_")[0]), poker)
                return point_list

        if querytype == self.QUERY_PAIR:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                return self.point_check(slotname,2)

        if querytype == self.QUERY_TWO_PAIR:
            return self.query(slotname, self.QUERY_PAIR)

        if querytype == self.QUERY_TRIPPLE:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                return self.point_check(slotname, 3)

        if querytype == self.QUERY_STRAIGHT:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                straight = self.point_check(slotname, 1)
                #small in first
                straight.sort()
                if len(straight) == 5 and (straight[1] - straight[0] == 1):
                    return straight
                else:
                    return []

        if querytype == self.QUERY_FLUSH:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                return self.color_check(slotname, 5)

        if querytype == self.QUERY_FULLHOUSE:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                looking_type_point = []
                pair = self.point_check(slotname, 2)
                tripple = self.point_check(slotname, 3)
                if len(pair) >= 1 and len(tripple) >=1:
                    looking_type_point.append(pair)
                    looking_type_point.append(tripple)
                return looking_type_point

        if querytype == self.QUERY_FOUR_OF_A_KIND:
            poker = self._dataslot[slotname]
            if poker == None:
                return []
            else:
                return self.point_check(slotname, 4)


    def copy_To(self, slotname,data ):
        self._dataslot[slotname] = data

    def get_remain_cards(self):
        remain = len(self._cards) - self._dealed_cards
        return remain

    def point_check(self,slotname,count_number,op = "=="):
        looking_type_point = []
        point_list = self.query(slotname, self.QUERY_POINT_ARR)
        # c = Counter('hello,world')
        # Counter({'l': 3, 'o': 2, 'e': 1, 'd': 1, 'h': 1, ',': 1, 'r': 1, 'w': 1})
        #return max(point_list)
        #cards_comb = list(itertools.combinations(cards, 3))
        #rest_cards = list(set(cards) - set(cards_comb[i]))
        c = Counter(point_list)
        for i in range(len(c)):
            key, value = c.popitem()
            if op == "==":
                if value == count_number:
                    looking_type_point.append(key)
            elif op == ">=":
                if value >= count_number:
                    looking_type_point.append(key)

        return looking_type_point

    def color_check(self, slotname, count_number):
        looking_type_list = []
        color_list = self.query(slotname, self.QUERY_COLOR)

        c = Counter(color_list)
        for i in range(len(c)):
            key, value = c.popitem()
            if value == count_number:
                looking_type_list.append(key)
        return looking_type_list

    def test_script(self, test_data):
        self._test_data = test_data