import os

import sys
sys.path.append("modules/msg_queue/zmqModual/")
sys.path.append("modules/")

from config_parser import * 

from msgworker import *
from msg_proxy import *

class msg_proxy(object):

      def __init__(self,module):
          self._module = module
          self._pid = os.getpid()
          print 'msg proxy %s is running ...' % self._pid


      def Receive(self):
#          while True:
#              self._module.receive()
          self._module.start()           

def main():
    # create any kind receiver module you want
    data = config_parser()

    proxy = msg_proxy(zmq_msg_proxy(data))
    proxy.Receive()
   

if __name__ == "__main__":
    main() 
