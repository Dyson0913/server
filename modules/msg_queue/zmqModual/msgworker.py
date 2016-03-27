import zmq
import json
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


import sys
#sys.path.append('../')

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

          self._module = module_load(module_list)
          self._module.dynamicLoadModules()

          self._context = zmq.Context()
          url = "tcp://"+self._domain + ":"

          #send from front 
          self.receiver = self._context.socket(zmq.PULL)
          front = url + str(self._front_push_port)
          self.receiver.connect(front)
          
          #send to front
          self._front_push = self._context.socket(zmq.PUSH)
          front_pull = url + str(self._front_pull_port)
          self._front_push.connect(front_pull)

          back_url = "tcp://"+self._domain + ":" + str(self._back_port)
          print "front to " + front + " front_pull " + front_pull + " back to " + back_url

          #push to back
          self._result_send = self._context.socket(zmq.PUSH)
          self._result_send.connect(back_url)


      def start(self):

          print "start"
          while True:
              json_msg = self.receiver.recv_json()
              result = self._module.execute_work(json_msg) 
              
              #report to back
              self._result_send.send_json(result)

              #del data just for db
              if 'for_db' in result:
                 del result['for_db']
                 del result['key']
                 
              #response to client
              self._front_push.send_json(result) 

def main():
    worker = zmqWorker('localhost',8899)
    worker.start()

if __name__ == "__main__":

    main()

