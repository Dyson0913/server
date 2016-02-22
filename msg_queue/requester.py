import os

import sys
sys.path.append("zmqModual/")

#import modual in diffenent implement
from msgrequest import *

#base 
class msg_sender(object):

    def __init__(self,module):
         self._module = module
         self._pid = os.getpid()

    def send(self,data):
         self._module.send(data)

def main():
   
    sender = msg_sender(zmq_request("7788"))
    dic = dict()
    dic['client_id'] = 1
    dic['client'] = "aa"
    sender.send(dic)

if __name__ == "__main__":
    
    main()
    while(True):
       pass
