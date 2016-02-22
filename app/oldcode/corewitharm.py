from state import *
from skydef import *

class ArmInitState(InitState):
    def __init__(self, context):
        super(ArmInitState, self).__init__(context, 5) #set timeout 5 sec
        self._reset_arm_state = ResetArmSubState(self, context)
        self._connect_arm_state = ConnectArmSubState(self, context)
        self._build_ans_state = BuildAnswerSubState(self, context)
        self._arm_shuffle_state = ArmShuffleSubState(self, context)
        self._reset_card_state = ResetCardSubState(self, context)
        self._arm_setting_state = ArmSettingSubState(self, context)

        #self._init_arm_setting_state = InitArmSettingSubState(self, context)


    def enter_state(self):
        super(ArmInitState, self).enter_state()
        self.set_state(self._reset_arm_state)

class ResetArmSubState(State):
    def __init__(self, context, server):
        
        super(ResetArmSubState, self).__init__(context, 5) #set timeout 5 sec
        self._server = server

    def update_time(self):
        if self.check_timeout():
            self._context.set_state(self._context._connect_arm_state)


    def enter_state(self):
        super(ResetArmSubState, self).enter_state()
        self._server.arm_reset()

        
class ConnectArmSubState(State):
    def __init__(self, context, server):
        super(ConnectArmSubState, self).__init__(context)
        self._server = server

    def update_time(self):
        if self.check_timeout():
            self._context.set_state(self._context._build_ans_state)

    def enter_state(self):
        super(ConnectArmSubState, self).enter_state()
        self._server.arm_connect()

class BuildAnswerSubState(State):
    def __init__(self, context, server):
        super(BuildAnswerSubState, self).__init__(context, 5) #set timeout 5 sec
        self._server = server
        self._sended_msg = False
        self._recv_build_msg = False

    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                if event['data'] == self._server.make_msg(SKY_BALL5_CMD_CONN_BUILD,0,0):
                    self._recv_build_msg = True
                elif self._recv_build_msg == True and event['data'] == self._server.make_msg(SKY_BALL5_CMD_EXE):
                    self._context.set_state(self._context._arm_shuffle_state)

    def enter_state(self):
        super(BuildAnswerSubState, self).enter_state()
        self._server.send_arm_msg(SKY_SERVER_CMD_CONN_BUILD, 32772, 2)
        self._sended_msg = True


class ArmShuffleSubState(State):
    def __init__(self, context, server):
        super(ArmShuffleSubState, self).__init__(context, 5) 
        self._server = server
        self._sended_msg = False

    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                if event['data'] == self._server.make_msg(SKY_BALL5_CMD_RECV_CMD):
                    self._context.set_state(self._context._reset_card_state)

    def enter_state(self):
        super(ArmShuffleSubState, self).enter_state()
        self._server.send_arm_msg(SKY_SERVER_CMD_START_SHUFFLE, SKY_SHUFFER_0, 1, 1) 
        self._sended_msg = True
        
class ResetCardSubState(State):
    def __init__(self, context, server):
        super(ResetCardSubState, self).__init__(context, 5) 
        self._server = server
        self._sended_msg = False

    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                if event['data'] == self._server.make_msg(SKY_BALL5_CMD_RECV_CMD):
                    self._context.set_state(self._context._arm_setting_state)

    def enter_state(self):
        super(ResetCardSubState, self).enter_state()
        self._server.send_arm_msg(SKY_SERVER_CMD_RESET_CARD_COUNT)
        self._sended_msg = True
        
class ArmSettingSubState(State):
    def __init__(self, context, server):
        super(ArmSettingSubState, self).__init__(context, 5) 
        self._server = server
        self._sended_msg = False

    def update_event(self, event):
        if self._sended_msg == True:
            if event['type'] == EVT_RECV_ARM_MSG:
                if event['data'] == self._server.make_msg(SKY_BALL5_CMD_RECV_CMD):
                    self._context.leave_state()

    def enter_state(self): 
        super(ArmSettingSubState, self).enter_state()
        self._server.send_arm_msg(SKY_SERVER_CMD_SET, 416, 8, 1040, 20)
        self._sended_msg = True
       
class ArmNewRoundState(NewRoundState):
    def update_time(self):
        super(ArmNewRoundState, self).update_time()
        if self.check_timeout():
            self.leave_state()

class ArmEndBetState(EndBetState):
    def update_time(self):
        super(ArmEndBetState, self).update_time()
        if self.check_timeout():
            self.leave_state()

class ArmEndRoundState(EndRoundState):
    def update_time(self):
        super(ArmEndRoundState, self).update_time()
        if self.check_timeout():
            self.leave_state()



