import datetime
from pylog import *
import time

import datetime, threading
from threading import Timer

class State(object):

    period = 0
    name = None
    default_state = None
    next_state = None

    def on_enter(self):
        self._state_time = time.time()
        logging.info( "on_enter " + self.name)
        self.enter()

    def enter(self):         
        self.execute()
        self.game.flush_state(self.name)
        self.game.player_list.broadcast(self.msg())
        #print self.msg()
        
    def execute(self):
        pass

    def default_State(self):
        self.next_state = self.default_state

    def next_state(self,next_state):
        self._next_state = next_state

    def on_update(self):
        self.update()

        # no need to update frequently,just flush after enter
        #self.game.flush_state(self.name)
#        print self.get_remain_time()

    def update(self):
        pass

    def msg(self):
        mymsg =  self.game.msg()
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


class fsm(object):
   
   def __init__(self):
       self._all_state ={}
       self._current_state = None
       self._stop_timer = False

   def add(self,state):
#       logging.info( "state_name = " + state._module.__class__.__name__ )
#       logging.info( "state_name = " + state.name )
       self._all_state[state.name] = state
       setattr(state,'game',self.game) 
       setattr(state,'fsm',self)

   def start(self,init_state):

       if self._all_state.has_key(init_state) == False:
           logging.info( "init state error "+ init_state )
           return

       self.kick(init_state)
       threading.Timer(0.1, self.time).start()
       return
       #self.timer = threading.Timer(1,self.on_update,args=["WOW"])
#       self.timer = threading.Timer(1,self.time)
#       self.timer.start()
   def delay_start(self, init_state,delay):

       threading.Timer(delay, self.start(init_state)).start()

   def time(self):

       if self._current_state.timeout():
           self.next()
       else:
           self._current_state.on_update()

       if self._stop_timer == False:
           threading.Timer(1, self.time).start()

   
   def stop(self):
       self._stop_timer = True 

   def next(self):
       self.transitions(self._current_state.next_state)

   def transitions(self,state_name):
#       logging.info("transistion to " + state_name)
       if self._all_state.has_key(state_name):
           #before trans A to B, reset A default state
           self._current_state.default_State()
           self.kick(state_name)

       else:
          logging.info("error !! no such state")

   def kick(self,init_state):
       state = self._all_state[init_state]
       self._current_state = state
       self._current_state.on_enter()

   def test_script(self,script_name,args):
       self.game.test_script(script_name,args)

   def init_msg(self):
       return self.game.init_msg()

   def msg(self):
       self.game.msg()


