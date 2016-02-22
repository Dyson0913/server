from poker import *
from state import *

class BigWinOpenState(State):
    def __init__(self, context):
        self._open_init_state = State(self)
        self._player_state = BigWinOpenPlayerSubState(self, context)
        self._banker_state = BigWinOpenBankerSubState(self, context)
        self._river_state = BigWinOpenRiverSubState(self, context)
        self._sub_state = self._open_init_state

        super(BigWinOpenState, self).__init__(context)
    
    def update_time(self):
        self._sub_state.update_time()


    def set_state(self, new_state):
        self._sub_state = new_state
        self._sub_state.enter_state()   

    def enter_state(self):
        self.set_state(self._player_state)
        super(BigWinOpenState, self).enter_state()

    def leave_state(self):
        self._context.set_state(self._context._end_round_state)


class BigWinOpenPlayerSubState(State):
   
    def __init__(self, context, game):
        self._game = game
        super(BigWinOpenPlayerSubState, self).__init__(context)

    def update_time(self):
        if self.check_timeout():
            self._context.set_state(self._context._banker_state)

    def enter_state(self):
        self._game.deal_player_card()
        super(BigWinOpenPlayerSubState, self).enter_state()

class BigWinOpenBankerSubState(State):
    BANKER_CARDS_NUM = 2
    def __init__(self, context, game):
        self._game = game
        super(BigWinOpenBankerSubState, self).__init__(context)

    def update_time(self):
        if self.check_timeout():
            if self._game.get_banker_card_num() == BigWinOpenBankerSubState.BANKER_CARDS_NUM:
                self._context.set_state(self._context._river_state)
            else:
                self._context.set_state(self._context._player_state)

    def enter_state(self):
        self._game.deal_banker_card()
        super(BigWinOpenBankerSubState, self).enter_state()

class BigWinOpenRiverSubState(State):
    def __init__(self, context, game):
        self._game = game
        super(BigWinOpenRiverSubState, self).__init__(context)

    def update_time(self):
        if self.check_timeout():
            self._context.leave_state()

    def enter_state(self):
        self._game.deal_river_card()
        super(BigWinOpenRiverSubState, self).enter_state()

class BigWin(object):

    def __init__(self):
        self.init_state = InitState(self)
        self._new_round_state = NewRoundState(self)
        self._end_bet_state = EndBetState(self)
        self._open_state = BigWinOpenState(self)
        self._end_round_state = EndRoundState(self)
        self._state = self.init_state
        self._banker = []
        self._player = []
        self._river = []
        self._poker = Poker()
        self.reset()

    @staticmethod
    def instance():
        if not hasattr(BigWin, '_instance'):
            BigWin._instance = BigWin()

        return BigWin._instance

    def set_state(self, new_state):
        self._state = new_state
        self._state.enter_state()

    def reset(self):
        del self._banker[:]
        del self._player[:]
        del self._river[:]
        self._poker.shuffle()

    def get_player_crd_num(self):
        return len(self._player)

    def get_banker_card_num(self):
        return len(self._banker)

    def deal_player_card(self):
        card = self._poker.deal_cards(1)
        self._player += card
        print "deal_player_card %s" % card

    def deal_banker_card(self):
        card = self._poker.deal_cards(1)
        self._banker += card
        print "deal_banker_card %s" % card

    def deal_river_card(self):
        card = self._poker.deal_cards(1)
        self._river += card
        print "deal_river_card %s" % card

    def check_game_state(self):
        self._state.update_time()

    def check_result(self):
        total_cards = self._banker + self._player + self._river
        print total_cards
        value = PokerPoint.check_big_win_show_hand(total_cards)
        if value != PokerPoint.POKER_NONE:
            print value
        else:
            print "POKER_NONE"
            banker_point = PokerPoint.get_baccarat_point(self._banker) 
            player_point = PokerPoint.get_baccarat_point(self._player)
            if banker_point > player_point:
                print "banker win"
            elif player_point > banker_point:
                print "player win"
            else:
                print "banker player tie"




