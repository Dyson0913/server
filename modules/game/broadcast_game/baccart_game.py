import sys
import os

sys.path.append('../')
sys.path.append('../broadcast_game')

from fsm import *
from poker import *
import pylog

from ba_paytable import *
import ba_paytable


class baccarat(object):
      
    def __init__(self):
        self._poker = Poker()
        self._player =[]
        self._banker =[]

    def reset(self):
        del self._banker[:]
        del self._player[:]
        self._poker.shuffle()

    def deal_player_card(self):
        card = self._poker.deal_cards(1)
        self._player += card
        logging.info( "player card " + str(self._player))

    def deal_banker_card(self):
        card = self._poker.deal_cards(1)
        self._banker += card
        logging.info( "banker card " + str(self._banker))

    def banker_extra_card(self):
        return PokerPoint.check_baccarat_banker_extra_card_rule(
            self._player,
            self._banker)

    def top_card_rule(self):
        return PokerPoint.check_baccarat_top_card_rule(self._player) or PokerPoint.check_baccarat_top_card_rule(self._banker)

    def get_banker_card_num(self):
        return len(self._banker)

    def player_extra_card(self):
        if self.get_banker_card_num() == 2:
            return PokerPoint.check_baccarat_player_extra_card_rule(
                self._player)
        else:
            return False

    def settle(self):
        logging.info( "settle" )
        playerpoint = PokerPoint.get_baccarat_point(self._player)
        bankerpoint = PokerPoint.get_baccarat_point(self._banker)
        winstate = ""
        if playerpoint > bankerpoint:
            logging.info("player win")
            winstate += ba_paytable.combine_winstate(Baccarat_player,ba_odds_1)
        elif playerpoint < bankerpoint:
            logging.info("banker win")
            winstate += ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        else:
            logging.info("tie")
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

class init(object):

    def __init__(self,game):
        self._game = game
        self._next_state = "wait_bet"

    def execute(self):
        self._game.reset()

class wait_bet(object):

    def __init__(self,game):
        self._game = game
        self._next_state = "player_card"

    def execute(self):
        pass

class player_card(object):

    def __init__(self,game):
        self._game = game
        self._next_state = "banker_card"

    def execute(self):
        self._game.deal_player_card()
        
        if self._game.banker_extra_card():
            self._next_state = "banker_card"
        else:
            self._next_state = "settle"
 

class banker_card(object):

    def __init__(self,game):
        self._game = game
        self._next_state = "player_card"

    def execute(self):
        self._game.deal_banker_card()

        if self._game.get_banker_card_num() < 2:
            return

        if self._game.top_card_rule():
            self._next_state = "settle"

        if self._game.player_extra_card():
            self._next_state = "player_card"
        else:
           if self._game.banker_extra_card():
              self._next_state = "banker_card"
           else:
              self._next_state = "settle"


class settle(object):

    def __init__(self,game):
        self._game = game
        self._next_state = "init"

    def execute(self):
        self._game.settle()

def main():
    
    mygame = baccarat()

    myfms = fms()
    myfms.add(State(init(mygame),1))
    myfms.add(State(wait_bet(mygame),1))
    myfms.add(State(player_card(mygame),2))
    myfms.add(State(banker_card(mygame),1))
    myfms.add(State(settle(mygame),1))

    myfms.start("init")

if __name__ == "__main__":
    main()

 
