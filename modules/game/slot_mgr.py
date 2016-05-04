import sys

sys.path.append('slot/')

from fsm import *
from hope_three import *

class game_mgr(object):

    def __init__(self,name):

        self._running_game = {}
        self._mgrname = name

    def spawn(self,game_module,room):
        
        #TODO open self_config game by client
        msg = self.create(game_module,room)
        return msg
 
#       wait in backi( match algo),ready, open a game to service


    def create(self,game,room):
        
        serial_id = game + "_" + room
        myfms = fms()
        mygame = None 
        if game == "hope":
            mygame = hope_three(serial_id,8,5,30)

        setattr(myfms,'game',mygame)
        setattr(myfms,'game_mgr',self)
        myfms.add(init(-1))
        myfms.add(NG(-1))
        myfms.add(FG(-1))
        myfms.add(JP(-1))

        myfms.start("init")

        self._running_game[serial_id] = myfms
        return myfms.init_msg()

    def del_game(self,game_id):
         
        game = self._running_game[game_id]
        game.stop()
         
        del self._running_game[game_id]
        del game

def main():
    
    ba_mgr = game_mgr("baccarat")
    ba_mgr.spawn()

if __name__ == "__main__":
    main()

