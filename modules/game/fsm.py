import datetime
from pylog import *
import time

import datetime, threading
from threading import Timer

class State(object):

    def __init__(self,state_unit,stay_period = 1):

        self._period = stay_period
        self._state_unit = state_unit
        self._next_state = state_unit._next_state
        #self.timer = threading.Timer(1,self.on_update,args=["WOW"])

    def on_enter(self):
        self._state_time = time.time()
        logging.info( "on_enter " + self._state_unit.__class__.__name__ )
        self._state_unit.execute()
        self._next_state = self._state_unit._next_state

    def on_update(self):
        pass
#        print self.get_remain_time()

    def msg(self):
        mymsg =  self._state_unit.msg()
        mymsg['rest_time'] = self.get_remain_time()
        return mymsg

    def timeout(self):
        timediff = time.time() - self._state_time
        if timediff > self._period:
            return True
        else:
            return False

    # can move out       
    def get_remain_time(self):
        timediff = time.time() - self._state_time
        
        if timediff > self._period:
            diff = self._period
        else:
            diff = self._period - int(timediff)

        return diff


class fms(object):
   
   def __init__(self):
       self._all_state ={}
       self._current_state = None

   def add(self,state):
#       logging.info( "state_name = " + state._module.__class__.__name__ )
       self._all_state[state._state_unit.__class__.__name__] = state

   def start(self,init_state):

       if self._all_state.has_key(init_state) == False:
           logging.info( "init state error "+ init_state )
           return

       self.kick(init_state)
       threading.Timer(0.1, self.time).start()

   def time(self):

       if self._current_state.timeout():
           self.transitions(self._current_state._next_state)
       else:
           self._current_state.on_update()

       threading.Timer(1, self.time).start()

   def transitions(self,state_name):
#       logging.info("transistion to " + state_name)
       if self._all_state.has_key(state_name):
           self.kick(state_name)
       else:
          logging.info("error !! no such state")

   def kick(self,init_state):
       state = self._all_state[init_state]
       self._current_state = state
       self._current_state.on_enter()

   def msg(self):
       self._current_state.msg()









