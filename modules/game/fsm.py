import datetime
from pylog import *
import time

import datetime, threading
from threading import Timer

class State(object):

    period = 0
    name = None
    next_state = None

    def on_enter(self):
        self._state_time = time.time()
        logging.info( "on_enter " + self.name)
        self.enter()

    def enter(self):         
        self.execute()
        self.app.flush_state(self.name)
#        self.app.msg()
        
    def execute(self):
        pass

    def next_state(self,next_state):
        self._next_state = next_state

    def on_update(self):
        self.update()
        self.app.flush_state(self.name)
#        print self.get_remain_time()

    def update(self):
        pass

    def msg(self):
        mymsg =  self.app.msg()
        mymsg['rest_time'] = self.get_remain_time()
        return mymsg

    def timeout(self):
       
        if self.period == -1:
            return False

        timediff = time.time() - self._state_time
        if timediff > self.period:
            return True
        else:
            return False

    # can move out       
    def get_remain_time(self):
        timediff = time.time() - self._state_time
        
        if timediff > self.period:
            diff = self.period
        else:
            diff = self.period - int(timediff)

        return diff


class fms(object):
   
   def __init__(self):
       self._all_state ={}
       self._current_state = None

   def add(self,state):
#       logging.info( "state_name = " + state._module.__class__.__name__ )
#       logging.info( "state_name = " + state.name )
       self._all_state[state.name] = state
       setattr(state,'app',self.app) 

   def start(self,init_state):

       if self._all_state.has_key(init_state) == False:
           logging.info( "init state error "+ init_state )
           return

       self.kick(init_state)
       threading.Timer(0.1, self.time).start()
       #self.timer = threading.Timer(1,self.on_update,args=["WOW"])

   def time(self):

       if self._current_state.timeout():
           self.next()
       else:
           self._current_state.on_update()

       threading.Timer(1, self.time).start()

   def next(self):
       self.transitions(self._current_state.next_state)

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

   def test_script(self,script_name,args):
       self.app.test_script(script_name,args)

   def msg(self):
       self.app.msg()









