import sys

sys.path.append('../')

from fsm import *
from poker import *
from pylog import *

from ba_paytable import *
import ba_paytable


class baccarat(object):
      
    def __init__(self,game_id):
        self._poker = Poker()
        self._poker.point_define(Poker.POINT_DEF_BACCART)
        self._info_to_client = None
        self._gameid = game_id
        #self._poker.test_script(["6_d","3_s","7_c","10_d","12_c","8_c"])


    def flush_state(self,state):
        msg = dict()
        msg['state'] = state
        msg['betzone'] = ba_paytable.bet_zone()
        msg['playerpoker'] = self._poker.query("playerPoker",Poker.QUERY_POKER)
        msg['bankerpoker'] = self._poker.query("BankerPoker",Poker.QUERY_POKER)
        msg['settle'] = self._paytable
        self._info_to_client = msg

    def test_script(self,script_name,args):
        self._poker.test_script(args)

    def init_msg(self):
        init = dict()
        init['game_id'] = self._gameid
        return init

    def msg(self):
        return self._info_to_client

    def reset(self):
        self._poker.add_slot("playerPoker")
        self._poker.add_slot("BankerPoker")
        self._paytable = []
        self._poker.shuffle()

    def deal_card(self,slotname):
        self._poker.deal_cards(1, slotname)

    def banker_extra_card(self):
        if self._poker.query("BankerPoker",Poker.QUERY_AMOUNT) != 2:
            return True

        bankerPoint = self._poker.query("BankerPoker",Poker.QUERY_Mod_10_Point)
        poker = self._poker.query("playerPoker", Poker.QUERY_POKER)
        self._poker.add_slot("lastPoker")
        self._poker.copy_To("lastPoker",poker[-1:])
        player_third_point = self._poker.query("lastPoker",Poker.QUERY_Mod_10_Point)

        if bankerPoint <= 2:
            return True

        if bankerPoint == 3:
            if player_third_point == 8:
                return False
            else:
                return True

        if bankerPoint == 4:
            if player_third_point == 0 or player_third_point == 1 or player_third_point == 8 or player_third_point == 9:
                return False
            else:
                return True

        if bankerPoint == 5:
            if player_third_point == 0 or player_third_point == 1 or player_third_point == 2 or player_third_point == 3 or player_third_point == 8 or player_third_point == 9:
                return False
            else:
                return True

        if bankerPoint == 6:

            if self._poker.query("playerPoker",Poker.QUERY_AMOUNT) != 3:
                return False
            else:
                if player_third_point == 6 or player_third_point == 7:
                    return True
                else:
                    return False

        return False

    def top_card_rule(self):
        if self._poker.query("playerPoker",Poker.QUERY_Mod_10_Point)  >=8 or self._poker.query("BankerPoker",Poker.QUERY_Mod_10_Point) >=8:
            return True
        return False

    def player_extra_card(self):
        if self._poker.query("playerPoker",Poker.QUERY_Mod_10_Point) >= 6:
            return False
        return True

    def get_banker_card_num(self):
        return self._poker.query("BankerPoker", Poker.QUERY_AMOUNT)

    def settle(self):
        logging.info( "settle" )
        playerpoint = self._poker.query("playerPoker",Poker.QUERY_Mod_10_Point)
        bankerpoint = self._poker.query("BankerPoker",Poker.QUERY_Mod_10_Point)
        winstate = ""

        if playerpoint > bankerpoint:
            winstate += ba_paytable.combine_winstate(Baccarat_player,ba_odds_1)
        elif playerpoint < bankerpoint:
            winstate += ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        else:
            winstate += ba_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
        # pair

        self._paytable = ba_paytable.paytable(winstate)
        logging.info("settle p point:" + str(playerpoint) + " b point " + str(bankerpoint) )
        logging.info( "settle" + str(self._paytable) )

        #TODO redis


class init(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.default_state = "wait_bet"
        self.next_state = self.default_state

    def execute(self):
        self.game.reset()

class wait_bet(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.default_state = "player_card"
        self.next_state = self.default_state

class player_card(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.default_state = "banker_card"
        self.next_state = self.default_state

    def execute(self):
        self.game.deal_card("playerPoker")
        
        if self.game.banker_extra_card():
            self.next_state = "banker_card"
        else:
            self.next_state = "settle"

class banker_card(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.default_state = "player_card"
        self.next_state = self.default_state

    def execute(self):
        self.game.deal_card("BankerPoker")

        if self.game.get_banker_card_num() < 2:
            return

        if self.game.get_banker_card_num() == 3:
            self.next_state = "settle"
            return

        if self.game.top_card_rule():
            self.next_state = "settle"
            return

        if self.game.player_extra_card():
            self.next_state = "player_card"
        else:
           if self.game.banker_extra_card():
              self.next_state = "banker_card"
           else:
              self.next_state = "settle"

class settle(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.default_state = "init"
        self.next_state = self.default_state

    def execute(self):
        self.game.settle()

def main():
    
    mygame = baccarat("main_baccarat")

    myfsm = fsm()
    setattr(myfsm,'game',mygame)
    myfsm.add(init(1))
    myfsm.add(wait_bet(10))
    myfsm.add(player_card(2))
    myfsm.add(banker_card(1))
    myfsm.add(settle(1))

    myfsm.start("init")

if __name__ == "__main__":
    main()

 
