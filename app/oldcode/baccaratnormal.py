from state import *
import pylog

class baccaratOpenState(State):

    def __init__(self, context):
        super(baccaratOpenState, self).__init__(context)
        self._open_init_state = State(self)
        self._player_state = baccaratOpenPlayerSubState(self, context)
        self._banker_state = baccaratOpenBankerSubState(self, context)
        self._player_extra_state = baccaratOpenPlayerExtraSubState(
            self,
            context)
        self._banker_extra_state = baccaratOpenBankerExtraSubState(
            self,
            context)
        self._sub_state = self._open_init_state

    def update_time(self):
        self._sub_state.update_time()

    def set_state(self, new_state):
        self._sub_state = new_state
        self._sub_state.enter_state()

    def enter_state(self):
        super(baccaratOpenState, self).enter_state()
        self.set_state(self._player_state)

    def leave_state(self):
        self._context.set_state(self._context._end_round_state)


class baccaratOpenPlayerSubState(State):

    def __init__(self, context, game):
        super(baccaratOpenPlayerSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
            self._context.set_state(self._context._banker_state)

    def enter_state(self):
        super(baccaratOpenPlayerSubState, self).enter_state()
        self._game.deal_player_card_from_poker()


class baccaratOpenPlayerExtraSubState(State):

    def __init__(self, context, game):
        super(baccaratOpenPlayerExtraSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
            if self._game.banker_extra_card():
                self._context.set_state(self._context._banker_extra_state)
            else:
                self._context.leave_state()

    def enter_state(self):
        super(baccaratOpenPlayerExtraSubState, self).enter_state()
        self._game.deal_player_card_from_poker()


class baccaratOpenBankerSubState(State):

    def __init__(self, context, game):
        super(baccaratOpenBankerSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
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
        super(baccaratOpenBankerSubState, self).enter_state()
        self._game.deal_banker_card_from_poker()


class baccaratOpenBankerExtraSubState(State):

    def __init__(self, context, game):
        super(baccaratOpenBankerExtraSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
            self._context.leave_state()

    def enter_state(self):
        super(baccaratOpenBankerExtraSubState, self).enter_state()
        self._game.deal_banker_card_from_poker()


