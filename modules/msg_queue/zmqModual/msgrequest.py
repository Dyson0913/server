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
        self._proxy_push_port = data["proxy_push_port"]
        self._proxy_pull_port = data["proxy_pull_port"]
        self._proxy_pub_port = data["proxy_pub_port"]

        url = "tcp://*:"
        self._context = zmq.Context()
        self._soc = self._context.socket(zmq.PUSH)
        push_url = url + str(self._proxy_push_port)
        self._soc.bind(push_url)

        #send from work
        self.receiver = self._context.socket(zmq.PULL)
        pull_url = url + str(self._proxy_pull_port)
        self.receiver.bind(pull_url)
        self.receiver = ZMQStream(self.receiver)
        self.receiver.on_recv(self.handle_worker_msg)
        print "push to " + push_url + "pull from" + pull_url

        
        self.pub_to_proxy = self._context.socket(zmq.PUB)
        pub_url = url + str(self._proxy_pub_port)
        self.pub_to_proxy.bind(pub_url)

 
    def send(self,data):
        
        #zmq can't serial object , need handle login and close in here 
        if data['cmd'] == 'login':
            add(data['client_id'],data['client'])
            del data['client']

        if data['cmd'] == 'self_close':
            uid = get_client_id(data['client'])
            if uid == None:
                print "return by no such a client"
                return
            else:
                #remove socket
                self_close_client = get(uid)
                remove(self_close_client)

            data['uuid'] = uid
            del data['client']

        self._soc.send_json(data)
        

    def handle_worker_msg(self,msg):
        
        #rece_json with [{data:value}], so get msg[0]
        parsed = json.loads(msg[0])
        #print parsed
        
        if parsed == None:
            print "handle work msg  error = None"
            return

        if 'cmd' in parsed:
            if parsed['cmd'] == 'login' or parsed['cmd'] == 'try_login':
                if parsed['state'] == 'login_ok':
                    #remove temp client_id ,using uuid
                    wait_login_client = get(parsed['client_id'])
                    remove(wait_login_client)
                    add(parsed['uuid'],wait_login_client)

                    #before send del client
                del parsed["client_id"]
                del parsed["cmd"]

        #proxy level msg TODO not find ,how to handle
        if 'trans' in parsed:
            print "get trans pass to other proxy "
            
            ip = parsed['trans']
            self.pub_to_proxy.send_multipart([str(1),str(msg[0])])
            #self.pub_to_proxy.send_json(parsed)
            #self._soc.send_json(parsed)
            return
       
        myclient = get(parsed['uuid'])

        if myclient == None:
            print "get client None"
            return

        myclient.write_message(parsed)

def main():    
    a = zmq_request(7788)

if __name__ == "__main__":

    main()
    while(True):
       pass

