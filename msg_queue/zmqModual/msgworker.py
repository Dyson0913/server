import zmq
import json
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


import sys
sys.path.append('../')

from  module_loader import *


class zmqWorker(object):

      def __init__(self,data):

          self._domain = data["domain"]
          self._front_push_port = data["front_push_port"]
          self._front_pull_port = data["front_pull_port"]
          self._back_port = data["back_port"]
          self._module_list =[];
          self._module_list.append( data['module']['auth'] )
          self._module_list.append( data['module']['lobby'] )
          modual_list = data["module"]['app']
          for item in modual_list:
              self._module_list.append( item['game'] )
          print self._module_list

          self._module = module_load(self._module_list)
          self._module.dynamicLoadModules()

          self._context = zmq.Context()
          url = "tcp://"+self._domain + ":"

          #send from front 
          self.receiver = self._context.socket(zmq.PULL)
          front = url + str(self._front_push_port)
          self.receiver.connect(front)
          print "link front to " + front
          
          #send to front
          self._front_push = self._context.socket(zmq.PUSH)
          front_pull = url + str(self._front_pull_port)
          self._front_push.connect(front_pull)
          print "link front pull to " + front_pull

          back_url = "tcp://"+self._domain + ":" + str(self._back_port)
          print "link back to " + back_url

          #push to back
          self._result_send = self._context.socket(zmq.PUSH)
          self._result_send.connect(back_url)


      def start(self):

          print "start"
          while True:
              work = self.receiver.recv_json()
              self.blocking_test(work);


      def receive(self,msg):
          msg = json.loads(msg[0])
          
          if msg['cmd'] == "close":
              pass
          print rep
          
      def blocking_test(self,work):
          if work['id'] == 2:
              self._send.send_json(work)
            
              print "fake return"
          else:
              print "normal"

              #send back to connect
              rep = dict()
              rep['message_type'] = "login"
              rep['result'] = 0
              rep['client_id'] = work['client_id']
              self._front_push.send_json(rep)

              self._send.send_json(work)
        

def main():
    worker = zmqWorker('localhost',8899)
    worker.start()

if __name__ == "__main__":

    main()

