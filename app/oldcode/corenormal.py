from state import *

class NormalInitState(InitState):
    def update_time(self):
        super(NormalInitState, self).update_time()
        if self.check_timeout():
            self.leave_state()

class NormalNewRoundState(NewRoundState):
    def update_time(self):
        super(NormalNewRoundState, self).update_time()
        if self.check_timeout():
            self.leave_state()

class NormalEndBetState(EndBetState):
    def update_time(self):
        super(NormalEndBetState, self).update_time()
        if self.check_timeout():
            self.leave_state()

class NormalEndRoundState(EndRoundState):
    def update_time(self):
        super(NormalEndRoundState, self).update_time()
        if self.check_timeout():
            self.leave_state()



