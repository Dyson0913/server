from state import *

class BigWinOpenState(State):

    def __init__(self, context):
        super(BigWinOpenState, self).__init__(context)
        self._open_init_state = State(self)
        self._player_state = BigWinOpenPlayerSubState(self, context)
        self._banker_state = BigWinOpenBankerSubState(self, context)
        self._river_state = BigWinOpenRiverSubState(self, context)
        self._sub_state = self._open_init_state

    def update_time(self):
        self._sub_state.update_time()

    def set_state(self, new_state):
        self._sub_state = new_state
        self._sub_state.enter_state()

    def enter_state(self):
        super(BigWinOpenState, self).enter_state()
        self.set_state(self._player_state)

    def leave_state(self):
        self._context.set_state(self._context._end_round_state)


class BigWinOpenPlayerSubState(State):

    def __init__(self, context, game):
        super(BigWinOpenPlayerSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
            self._context.set_state(self._context._banker_state)

    def enter_state(self):
        super(BigWinOpenPlayerSubState, self).enter_state()
        self._game.deal_player_card_from_poker()


class BigWinOpenBankerSubState(State):
    BANKER_CARDS_NUM = 2

    def __init__(self, context, game):
        super(BigWinOpenBankerSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
            if self._game.get_banker_card_num(
            ) == BigWinOpenBankerSubState.BANKER_CARDS_NUM:
                self._context.set_state(self._context._river_state)
            else:
                self._context.set_state(self._context._player_state)

    def enter_state(self):
        super(BigWinOpenBankerSubState, self).enter_state()
        self._game.deal_banker_card_from_poker()


class BigWinOpenRiverSubState(State):

    def __init__(self, context, game):
        super(BigWinOpenRiverSubState, self).__init__(context)
        self._game = game

    def update_time(self):
        if self.check_timeout():
            self._context.leave_state()

    def enter_state(self):
        super(BigWinOpenRiverSubState, self).enter_state()
        self._game.deal_river_card_from_poker()


