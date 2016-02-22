from state import *
from skydef import *
from poker import *

class PerfectAngelArmOpenState(State):
    def __init__(self, context):
        super(PerfectAngelArmOpenState, self).__init__(context)
        self._open_init_state = State(self)
        self._push_state = PushCardSubState(self, context)
        self._player_state = PerfectAngelArmOpenPlayerSubState(self, context)
        self._banker_state = PerfectAngelArmOpenBankerSubState(self, context)
        self._sub_state = self._open_init_state


    def enter_state(self):
        super(PerfectAngelArmOpenState, self).enter_state()
        self.set_state(self._push_state)
    
    def leave_state(self):
        self._context.set_state(self._context._end_round_state)

class PushCardSubState(State):
    
    def __init__(self, context, game):
        super(PushCardSubState, self).__init__(context)
        self._game = game
        self._sended_msg = False
    
    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                parsed = event['data'].split(",")
                if parsed[0] == "118" and parsed[2] == "2":
                    self._context.set_state(self._context._player_state)
   		
    def enter_state(self):
        super(PushCardSubState, self).enter_state()
        self._game.send_arm_msg(SKY_SERVER_CMD_SHUFFLE_DEAL, SKY_SHUFFER_0) 
        self._sended_msg = True
   

class PerfectAngelArmOpenPlayerSubState(State):
   
    PLAYER_CARDS_NUM = 5

    def __init__(self, context, game):
        super(PerfectAngelArmOpenPlayerSubState, self).__init__(context)
        self._game = game
        self._sended_msg = False
        
    def update_event(self, event):
        logging.info("PerfectAngelArmOpenPlayerSubState update_event {0}".format(event))
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                parsed = event['data'].split(",")
                if int(parsed[0]) == SKY_BALL5_CMD_OPEN_CARD:
                    card = PokerPoint.get_sky_card_map(int(parsed[2])) 
                    self._game.deal_player_card(card)
                elif int(parsed[0]) == SKY_BALL5_CMD_EXE:
                    self._context.set_state(self._context._banker_state)


    def enter_state(self):
        super(PerfectAngelArmOpenPlayerSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True
                 
class PerfectAngelArmOpenBankerSubState(State):
    BANKER_CARDS_NUM = 5
    def __init__(self, context, game):
        super(PerfectAngelArmOpenBankerSubState, self).__init__(context)
        self._game = game
        self._sended_msg = False
    

    def update_event(self, event):
        logging.info("PerfectAngelArmOpenBankerSubState update_event {0}".format(event))
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                parsed = event['data'].split(",")
                if int(parsed[0]) == SKY_BALL5_CMD_OPEN_CARD:
                    card = PokerPoint.get_sky_card_map(int(parsed[2]))
                    self._game.deal_banker_card(card)
                elif int(parsed[0]) == SKY_BALL5_CMD_EXE:
                    if self._game.get_banker_card_num() == PerfectAngelArmOpenBankerSubState.BANKER_CARDS_NUM:
                        self._context.leave_state()
                    else:
                        self._context.set_state(self._context._player_state)



    def enter_state(self):
        super(PerfectAngelArmOpenBankerSubState, self).enter_state()
        self._game.send_deal_card_msg()
        self._sended_msg = True
        
