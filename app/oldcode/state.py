import datetime
from pylog import *

STATE_INITIAL = 0
STATE_NEW_ROUND = 1
STATE_END_BET = 2
STATE_START_ROUND = 3
STATE_END_ROUND = 4

class State(object):
    def __init__(self, context, timeout = 3):
        self._context = context
        self._timeout = datetime.timedelta(seconds=timeout)
        self._state_time = datetime.datetime.now()
        self._sub_state = None

    def set_state(self, new_state):
        self._sub_state = new_state
        self._sub_state.enter_state()

    def check_timeout(self):
        timediff = datetime.datetime.now() - self._state_time
        if timediff > self._timeout:
            return True

    def update_event(self, event):
        if self._sub_state != None:
            self._sub_state.update_event(event)

    def update_time(self):
        #print "State update_time"
        if self._sub_state != None:
            self._sub_state.update_time()

    def enter_state(self):
        self._state_time = datetime.datetime.now()
        print self.__class__.__name__

    def get_remain_time(self):
        timediff = datetime.datetime.now() - self._state_time
        
        if timediff > self._timeout:
            diff = self._timeout
        else:
            diff = self._timeout - timediff

        return diff.seconds 

    def leave_state(self):
        pass

class InitState(State):
    def enter_state(self):
        super(InitState, self).enter_state()
        logging.info( "InitState" )
       
    def leave_state(self):
        self._context.set_state(self._context._new_round_state)

class NewRoundState(State):
  
    def enter_state(self):
        super(NewRoundState, self).enter_state()
        logging.info( "NewRoundState" )
        self._context.newround()
    
    def leave_state(self):
        self._context.set_state(self._context._end_bet_state)

class EndBetState(State):

    def enter_state(self):
        super(EndBetState, self).enter_state()
        logging.info( "EndBetState" )
        self._context.endbet()

    def leave_state(self):
        self._context.set_state(self._context._open_state)

    
class EndRoundState(State):
    
    def enter_state(self):
        super(EndRoundState, self).enter_state()
        logging.info( "EndRoundState" )
        self._context.check_result()

    def leave_state(self):
        self._context.set_state(self._context._new_round_state)

