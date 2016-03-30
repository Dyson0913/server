import sys

sys.path.append('broadcast_game/')

from fsm import *
from baccart_game import *

class game_mgr(object):

    def __init__(self,name):

        self._running_game = {}
        self._mgrname = name

    def order(self,json_msg):
        
       #if json_msg['cmd'] == "request_join":
       if json_msg['cmd'] == "request_open":
          #TODO open self_config game by client
#          json_msg['config']
           msg = self.spawn()
           return msg
 
#       wait in backi( match algo),ready, open a game to service


    def spawn(self):

        serial_id = self._mgrname + str(len(self._running_game))
        new_game = baccarat(serial_id)
        myfms = fms()
        myfms.add(State(init(new_game),1))
        myfms.add(State(wait_bet(new_game),1))
        myfms.add(State(player_card(new_game),2))
        myfms.add(State(banker_card(new_game),1))
        myfms.add(State(settle(new_game),1))
        myfms.start("init")

        self._running_game[serial_id] = myfms
        return myfms.msg()


def main():
    
    ba_mgr = game_mgr("baccarat")
    ba_mgr.spawn()

if __name__ == "__main__":
    main()

