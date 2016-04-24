import sys

sys.path.append('slot/')

from fsm import *
from hope_three import *

class game_mgr(object):

    def __init__(self,name):

        self._running_game = {}
        self._mgrname = name

    def order(self,json_msg):
        
       #if json_msg['cmd'] == "request_join":
  #     if json_msg['cmd'] == "request_open":
          #TODO open self_config game by client
#          json_msg['config']
        msg = self.spawn()
        return msg
 
#       wait in backi( match algo),ready, open a game to service


    def spawn(self):
        
        serial_id = self._mgrname + str(len(self._running_game))
        mygame = hope_three(serial_id,8,5,30)

        myfms = fms()
        setattr(myfms,'app',mygame)
        myfms.add(init(-1))
        myfms.add(NG(-1))
        myfms.add(FG(-1))
        myfms.add(JP(-1))

        myfms.start("init")

        self._running_game[serial_id] = myfms
        return myfms.msg()


def main():
    
    ba_mgr = game_mgr("baccarat")
    ba_mgr.spawn()

if __name__ == "__main__":
    main()

