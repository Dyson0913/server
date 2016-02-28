import os

import sys
sys.path.append("zmqModual/")

from msgworker import *

class questWorker(object):

      def __init__(self,module):
          self._module = module
          self._pid = os.getpid()
          print 'Worker %s is running ...' % self._pid


      def Receive(self):
#          while True:
#              self._module.receive()
          self._module.start()           

def main():
    # create any kind receiver module you want
    work = questWorker(zmqWorker('localhost',8899))
    work.Receive()
   

if __name__ == "__main__":
    main() 
