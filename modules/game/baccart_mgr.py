import sys

sys.path.append('broadcast_game/')

from fsm import *
from baccarat import *


from player import *

class game_mgr(object):

    def __init__(self,name):

        self._running_game = {}
        self._mgrname = name

    def spawn(self,serial_id,uid,player_socket):

        mygame = baccarat(serial_id)

        playerlist = player_list()
        player = player_info(uid, player_socket)
        playerlist.add_player(player)
        setattr(mygame, 'player_list', playerlist)
        setattr(mygame, 'proxy_socket', player_socket)

        myfsm = fsm()
        setattr(myfsm,'game',mygame)
        myfsm.add(init(2))
        myfsm.add(wait_bet(10))
        myfsm.add(player_card(3))
        myfsm.add(banker_card(3))
        myfsm.add(settle(5))
        myfsm.delay_start("init",1)

        self._running_game[serial_id] = myfsm
        return myfsm.init_msg()

    def del_game(self, game_id):

        if self._running_game.has_key(game_id) == False:
            return

        game = self._running_game[game_id]
        game.stop()

        del self._running_game[game_id]
        del game

    def join_game(self, game_id,uid,player_socket):
        if self._running_game.has_key(game_id) == False:
            return

        gamefsm = self._running_game[game_id]

        #add player to game
        player = player_info(uid, player_socket)
        gamefsm.game.player_list.add_player(player)
        return gamefsm.init_msg()

    def remove_player(self,game_id,uid):
        if self._running_game.has_key(game_id) == False:
            return

        gamefsm = self._running_game[game_id]
        gamefsm.game.player_list.remove_player(uid)


def main():
    
    ba_mgr = game_mgr("baccarat")
    ba_mgr.spawn()

if __name__ == "__main__":
    main()

