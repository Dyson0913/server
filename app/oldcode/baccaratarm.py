from state import *
from skydef import *
from poker import *
import pylog

class baccaratArmOpenState(State):

    def __init__(self, context):
        super(baccaratArmOpenState, self).__init__(context)
        self._open_init_state = State(self)
        self._player_state = baccaratArmOpenPlayerSubState(self, context)
        self._banker_state = baccaratArmOpenBankerSubState(self, context)
        self._player_extra_state = baccaratArmOpenPlayerExtraSubState(
            self,
            context)
        self._banker_extra_state = baccaratArmOpenBankerExtraSubState(
            self,
            context)
        self._sub_state = self._open_init_state

    def update_time(self):
        self._sub_state.update_time()

    def update_event(self, event):
        self._sub_state.update_event(event)

    def set_state(self, new_state):
        self._sub_state = new_state
        self._sub_state.enter_state()

    def enter_state(self):
        super(baccaratArmOpenState, self).enter_state()
        self.set_state(self._player_state)

    def leave_state(self):
        self._context.set_state(self._context._end_round_state)


class baccaratArmOpenPlayerSubState(State):

    def __init__(self, context, game):
        super(baccaratArmOpenPlayerSubState, self).__init__(context)
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
        super(baccaratArmOpenPlayerSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True


class baccaratArmOpenPlayerExtraSubState(State):

    def __init__(self, context, game):
        super(baccaratArmOpenPlayerExtraSubState, self).__init__(context)
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
                    if self._game.banker_extra_card():
                        self._context.set_state(self._context._banker_extra_state)
                    else:
                        self._context.leave_state()

    def enter_state(self):
        super(baccaratArmOpenPlayerExtraSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True



class baccaratArmOpenBankerSubState(State):

    def __init__(self, context, game):
        super(baccaratArmOpenBankerSubState, self).__init__(context)
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
                    if self._game.get_banker_card_num() == 2:
                        if self._game.player_top_card_rule():
                            self._context.leave_state()
                        else:
                           if self._game.player_extra_card():
                               self._context.set_state(self._context._player_extra_state)
                           else:
                               if self._game.banker_extra_card():
                                   self._context.set_state(self._context._banker_extra_state)
                               else:
                                   self._context.leave_state()
                    else:
                        self._context.set_state(self._context._player_state)
    

    def enter_state(self):
        super(baccaratArmOpenBankerSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True

class baccaratArmOpenBankerExtraSubState(State):

    def __init__(self, context, game):
        super(baccaratArmOpenBankerExtraSubState, self).__init__(context)
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
                    self._context.leave_state()

    def enter_state(self):
        super(baccaratArmOpenBankerExtraSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True



