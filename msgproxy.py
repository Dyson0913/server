import os

import socket


import sys
sys.path.append("modules/msg_queue/zmqModual/")
sys.path.append("modules/")

from config_parser import * 

#from msgworker import *
from msg_proxy import *

class msg_proxy(object):

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

          self._module.set_identity(str(local_ip)+ "_" + str(self._pid))
          print 'msg Worker %s is running ...' % self._pid + local_ip

      def Receive(self):
          self._module.start()           

def main():
    # create any kind receiver module you want
    data = config_parser()

    proxy = msg_proxy(zmq_msg_proxy(data))
    proxy.Receive()
   

if __name__ == "__main__":
    main() 
