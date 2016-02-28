import zmq
from zmq.eventloop.zmqstream import ZMQStream

#zmq ioloop conflact with tornado ioloop,need call 
from zmq.eventloop import ioloop
#ioloop.install()

# asap befort tonado ioloop
# reference https://pyzmq.readthedocs.org/en/latest/eventloop.html

import uuid
import json

import sys
sys.path.append('../')

from socketmgr import *

class zmq_request(object):

    def __init__(self,port):

         self._context = zmq.Context()
         #self._socket = self._context.socket(zmq.REQ)
         #self.stream = ZMQStream(self._socket)
         #self.stream.on_recv(self.handle_reply)
         self._soc = self._context.socket(zmq.PUSH)
         url = "tcp://*:" + str(port)
         print url
         self._soc.bind(url)

    def send(self,data):
        
        #zmq can't serial object , need handle login and close in here 
        if data['cmd'] == 'login':
            add(data['client_id'],data['client'])
            del data['client']

        if data['cmd'] == 'close':
            remove(data['client'])            
            del data['client']
            return

#        if data['cmd'] == 'request':
        #self._socket.send_json(data)
        self._soc.send_json(data)

    def handle_reply(self,msg):
        print "handle_reply  %s" % msg

        #rece_json with [{data:value}], so get msg[0]
        parsed = json.loads(msg[0])
        client_id = parsed['client_id']

        myclient = get(client_id)

        #ws
        myclient.write_message(parsed)

def main():    
    a = zmq_request(7788)

if __name__ == "__main__":

    main()
    while(True):
       pass

