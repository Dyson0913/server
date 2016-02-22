from state import *

class PerfectAngelOpenState(State):
    def __init__(self, context):
        self._open_init_state = State(self)
        self._player_state = PerfectAngelOpenPlayerSubState(self, context)
        self._banker_state = PerfectAngelOpenBankerSubState(self, context)
        self._sub_state = self._open_init_state

        super(PerfectAngelOpenState, self).__init__(context)
    

    def enter_state(self):
        self.set_state(self._player_state)
        super(PerfectAngelOpenState, self).enter_state()

    def leave_state(self):
        self._context.set_state(self._context._end_round_state)

    

class PerfectAngelOpenPlayerSubState(State):
   
    PLAYER_CARDS_NUM = 5

    def __init__(self, context, game):
        self._game = game
        super(PerfectAngelOpenPlayerSubState, self).__init__(context,3)

    def update_time(self):
        if self.check_timeout():
            self._context.set_state(self._context._banker_state)

    def enter_state(self):
        self._game.deal_player_card_from_poker()
        super(PerfectAngelOpenPlayerSubState, self).enter_state()

         
class PerfectAngelOpenBankerSubState(State):
    BANKER_CARDS_NUM = 5
    def __init__(self, context, game):
        self._game = game
        super(PerfectAngelOpenBankerSubState, self).__init__(context,3)

    def update_time(self):
        if self.check_timeout():
            if self._game.get_banker_card_num() == PerfectAngelOpenBankerSubState.BANKER_CARDS_NUM:
                self._context.leave_state()
            else:
                self._context.set_state(self._context._player_state)

    def enter_state(self):
        self._game.deal_banker_card_from_poker()
        super(PerfectAngelOpenBankerSubState, self).enter_state()


