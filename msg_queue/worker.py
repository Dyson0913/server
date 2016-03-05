import os

import sys
sys.path.append("zmqModual/")

from optparse import OptionParser

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
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage)
    parser.add_option("-f", "--file", default="worker1.json")
    (options, args) = parser.parse_args()

    config_file = open(options.file)
    data = json.load(config_file)

    work = questWorker(zmqWorker(data))
    work.Receive()
   

if __name__ == "__main__":
    main() 
