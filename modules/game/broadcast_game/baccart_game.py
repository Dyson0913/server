import sys

sys.path.append('../')

from fsm import *
from poker import *
from pylog import *

from ba_paytable import *
import ba_paytable


class baccarat(object):
      
    def __init__(self,name):
        self._poker = Poker()
        self._poker.add_slot("playerPoker")
        self._poker.add_slot("BankerPoker")
        self._poker.point_define(Poker.POINT_DEF_BACCART)
        self._player =[]
        self._banker =[]
        self._win = ""
        self._name = name
        self._info_to_client = None 

    def flush_state(self,state):
        msg = dict()
        msg['state'] = state
        msg['playerpoker'] = self._player
        msg['bankerpoker'] = self._banker

        self._info_to_client = msg

    def test_script(self,script_name,args):
        self._poker.test_script(args)

    def msg(self):
        logging.info( "client msg " + str(self._info_to_client))
        return self._info_to_client

    def reset(self):
        del self._banker[:]
        del self._player[:]
        self._poker.shuffle()

    def deal_card(self,slotname):
        self._poker.deal_cards(1, slotname)

    def banker_extra_card(self):
        if self.get_banker_card_num() != 2:
            return True

        return PokerPoint.check_baccarat_banker_extra_card_rule(self._player, self._banker)

    def top_card_rule(self):
        if self._poker.query("playerPoker",Poker.QUERY_POINT) >=8 or self._poker.query("BankerPoker",Poker.QUERY_POINT) >=8:
            return True
        return False

    def get_banker_card_num(self):
        return self._poker.query("BankerPoker",Poker.QUERY_AMOUNT)

    def player_extra_card(self):
        if self._poker.query("playerPoker",Poker.QUERY_POINT) >= 6:
            return False
        return True


    def settle(self):
        logging.info( "settle" )
        playerpoint = PokerPoint.get_baccarat_point(self._player)
        bankerpoint = PokerPoint.get_baccarat_point(self._banker)
        winstate = ""
        
        logging.info( "settle p point:" + str(playerpoint) +" b point "+ str(bankerpoint))
        if playerpoint > bankerpoint:
            logging.info("player win")
            self._win = "player win"
            winstate += ba_paytable.combine_winstate(Baccarat_player,ba_odds_1)
        elif playerpoint < bankerpoint:
            logging.info("banker win")
            self._win = "banker win"
            winstate += ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        else:
            logging.info("tie")
            self._win = "tie"
            winstate += ba_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
            # pair
            # playerpoint = PokerPoint.get_baccarat_point(self.playerpoker[2:])
            # bankerpoint = PokerPoint.get_baccarat_point(self.bankerpoker[2:])
            # if playerpoint > bankerpoint:
            #     winstate = Baccarat.wintype_pair

        #msg['winstate'] = winstate
        logging.info( "settle" + str(ba_paytable.paytable(winstate)) )
#        msg['paytable'] = ba_paytable.paytable(winstate)
#        msg['message_type'] = MSG_TYPE_ROUND_INFO

        #TODO redis
#        self.publish(msg)


class init(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "wait_bet" 

    def execute(self):
        self.game.reset()

class wait_bet(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "player_card"

class player_card(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "banker_card"

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
        self.next_state = "player_card"

    def execute(self):
        self.game.deal_card("BankerPoker")

        if self.game.get_banker_card_num() < 2:
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
        self.next_state = "init"

    def execute(self):
        self.game.settle()

def main():
    
    mygame = baccarat("main_baccarat")

    myfsm = fsm()
    setattr(myfsm,'game',mygame)
    myfsm.add(init(1))
    myfsm.add(wait_bet(1))
    myfsm.add(player_card(2))
    myfsm.add(banker_card(1))
    myfsm.add(settle(1))

    myfsm.start("init")

if __name__ == "__main__":
    main()

 
