import os

import socket

import sys
sys.path.append("modules/msg_queue/zmqModual/")
sys.path.append("modules/")

sys.path.append("modules/db")
sys.path.append("modules/db/noSQL")
sys.path.append('modules/game')
sys.path.append('modules/game/slot/')
sys.path.append('modules/game/broadcast_game/')
sys.path.append('modules/bet')
sys.path.append('modules/settle')


from config_parser import * 

from msg_worker import *

class questWorker(object):

      def __init__(self,module):
          self._module = module
          self._pid = os.getpid()
          
          #private ip
          local_ip = socket.gethostbyname(socket.gethostname())
          #print "private ip:%s "% local_ip

          #private ip 2
          #myname = socket.getfqdn(socket.gethostname())
          #myaddr = socket.gethostbyname(myname)
          #print "local ip:%s "% myaddr

          self._module.set_identity(str(local_ip))
          print 'msg Worker %s is running ...' % self._pid + local_ip


      def Receive(self):
          self._module.start()           

def main():
    # create any kind receiver module you want
    data = config_parser()

    work = questWorker(msgworker(data))
    work.Receive()
   

if __name__ == "__main__":
    main() 
