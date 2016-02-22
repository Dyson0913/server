from state import *
from skydef import *
from poker import *
import pylog

class BigWinArmOpenState(State):

    def __init__(self, context):
        super(BigWinArmOpenState, self).__init__(context)
        self._open_init_state = State(self)
        self._player_state = BigWinArmOpenPlayerSubState(self, context)
        self._banker_state = BigWinArmOpenBankerSubState(self, context)
        self._river_state = BigWinArmOpenRiverSubState(self, context)
        self._sub_state = self._open_init_state
    
    def enter_state(self):
        super(BigWinArmOpenState, self).enter_state()
        self.set_state(self._player_state)

    def leave_state(self):
        self._context.set_state(self._context._end_round_state)


class BigWinArmOpenPlayerSubState(State):

    def __init__(self, context, game):
        super(BigWinArmOpenPlayerSubState, self).__init__(context)
        self._game = game
        self._sended_msg = False

    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                parsed = event['data'].split(",")
                if parsed[0] == "111":
                    card = PokerPoint.get_sky_card_map(int(parsed[2])) 
                    self._game.deal_player_card(card)
                elif parsed[0] == "134":
                    self._context.set_state(self._context._banker_state)


    def enter_state(self):
        super(BigWinArmOpenPlayerSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True



class BigWinArmOpenBankerSubState(State):
    BANKER_CARDS_NUM = 2

    def __init__(self, context, game):
        super(BigWinArmOpenBankerSubState, self).__init__(context)
        self._game = game
        self._sended_msg = False
    
    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                parsed = event['data'].split(",")
                if parsed[0] == "111":
                    card = PokerPoint.get_sky_card_map(int(parsed[2])) 
                    self._game.deal_banker_card(card)
                elif parsed[0] == "134":
                    if self._game.get_banker_card_num(
                    ) == BigWinArmOpenBankerSubState.BANKER_CARDS_NUM:
                        self._context.set_state(self._context._river_state)
                    else:
                        self._context.set_state(self._context._player_state)

    def enter_state(self):
        super(BigWinArmOpenBankerSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True

class BigWinArmOpenRiverSubState(State):

    def __init__(self, context, game):
        super(BigWinArmOpenRiverSubState, self).__init__(context)
        self._game = game
        self._sended_msg = False

    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                parsed = event['data'].split(",")
                if parsed[0] == "111":
                    card = PokerPoint.get_sky_card_map(int(parsed[2])) 
                    self._game.deal_river_card(card)
                elif parsed[0] == "134":
                    self._context.leave_state()

    def enter_state(self):
        super(BigWinArmOpenRiverSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True



