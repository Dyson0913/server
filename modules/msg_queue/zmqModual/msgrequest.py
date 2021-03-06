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
#sys.path.append('../')

from socketmgr import *

class zmq_request(object):

    def __init__(self,data):

        self._domain = data["domain"]
        self._front_push_port = data["front_push_port"]
        self._front_pull_port = data["front_pull_port"]

        url = "tcp://*:"
        self._context = zmq.Context()
        self._soc = self._context.socket(zmq.PUSH)
        push_url = url + str(self._front_push_port)
        self._soc.bind(push_url)

        #send from work
        self.receiver = self._context.socket(zmq.PULL)
        pull_url = url + str(self._front_pull_port)
        self.receiver.bind(pull_url)

        self.receiver = ZMQStream(self.receiver)
        self.receiver.on_recv(self.handle_worker_msg)
        print "push to " + push_url + "pull from" + pull_url
 
    def send(self,data):
        
        #zmq can't serial object , need handle login and close in here 
        if data['cmd'] == 'login':
            add(data['client_id'],data['client'])
            del data['client']

        if data['cmd'] == 'self_close':
            data['client_id'] = get_client_id(data['client'])
            del data['client']

        self._soc.send_json(data)

    def handle_worker_msg(self,msg):
        #print "handle_reply  %s" % msg
        
        #rece_json with [{data:value}], so get msg[0]
        parsed = json.loads(msg[0])

        if parsed == None:
            print "handle work msg  error = None"
            return

        if 'cmd' in parsed:
            if parsed['cmd'] == 'login':
                #remove temp client_id ,using uuid
                wait_login_client = get(parsed['client_id'])
                remove(wait_login_client)
                add(parsed['uuid'],wait_login_client)

                #before send del client
                del parsed["client_id"]
                del parsed["cmd"]

            #handle self close
            elif parsed['cmd'] == "self_close":
                self_close_client = get(parsed['client_id'])
                remove(self_close_client)
                print "client self close"
                return

        myclient = get(parsed['uuid'])

        if myclient == None:
            print "get client None error"
            return

        myclient.write_message(parsed)

def main():    
    a = zmq_request(7788)

if __name__ == "__main__":

    main()
    while(True):
       pass

