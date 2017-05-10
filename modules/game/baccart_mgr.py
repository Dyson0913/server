import sys

sys.path.append('broadcast_game/')

from fsm import *
from baccarat import *

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
        myfsm = fsm()
        setattr(myfsm,'game',new_game)
        myfsm.add(init(1))
        myfsm.add(wait_bet(1))
        myfsm.add(player_card(2))
        myfsm.add(banker_card(1))
        myfsm.add(settle(1))
        myfsm.start("init")

        self._running_game[serial_id] = myfsm
        return myfsm.msg()


def main():
    
    ba_mgr = game_mgr("baccarat")
    ba_mgr.spawn()

if __name__ == "__main__":
    main()

