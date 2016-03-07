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
          module_list =[]
          module_list.append( data['module']['auth'] )
          module_list.append( data['module']['lobby'] )
          modual_list = data["module"]['app']
          for item in modual_list:
              module_list.append( item['game'] )
          print module_list

          self._module = module_load(module_list)
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
              json_msg = self.receiver.recv_json()
              result = self._module.execute_work(json_msg) 
              
              #response to client
              self._front_push.send_json(result) 

              #report to back
              self._result_send.send_json(result)

      def receive(self,msg):
          msg = json.loads(msg[0])
          
          if msg['cmd'] == "close":
              pass
          print rep

        

def main():
    worker = zmqWorker('localhost',8899)
    worker.start()

if __name__ == "__main__":

    main()

