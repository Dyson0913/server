import sys

sys.path.append('broadcast_game/')

from fsm import *
from baccarat import *


from player import *

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


    def spawn(self,game,room,player_info):

        serial_id = game + "_" + room
        myfsm = fsm()
        mygame = baccarat(serial_id)

        playerlist = player_list()
        playerlist.add_player(player_info)
        setattr(mygame, 'player_list', playerlist)

        setattr(myfsm,'game',mygame)
        myfsm.add(init(2))
        myfsm.add(wait_bet(10))
        myfsm.add(player_card(3))
        myfsm.add(banker_card(3))
        myfsm.add(settle(5))
        myfsm.start("init")

        self._running_game[serial_id] = myfsm
        return myfsm.init_msg()

    def del_game(self, game_id):
        game = self._running_game[game_id]
        game.stop()

        del self._running_game[game_id]
        del game

def main():
    
    ba_mgr = game_mgr("baccarat")
    ba_mgr.spawn()

if __name__ == "__main__":
    main()

