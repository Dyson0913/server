import os

import sys
sys.path.append("modules/msg_queue/zmqModual/")
sys.path.append("modules/")

from config_parser import * 

from msg_worker import *

class questWorker(object):

      def __init__(self,module):
          self._module = module
          self._pid = os.getpid()
          print 'msg Worker %s is running ...' % self._pid


      def Receive(self):
          self._module.start()           

def main():
    # create any kind receiver module you want
    data = config_parser()

    work = questWorker(msgworker(data))
    work.Receive()
   

if __name__ == "__main__":
    main() 
