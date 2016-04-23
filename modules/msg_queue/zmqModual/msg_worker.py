import zmq
import json

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop

import sys
sys.path.append('../../')

from  module_loader import *

ioloop.install()


class msgworker(object):

      def __init__(self,data):

          self._domain = data["domain"]

          # load module
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

          #send from broker 
          self.recever = self._context.socket(zmq.PULL)
          front = url + str(data["broker_to_worker_back_port"])
          self.recever.connect(front)
          self.recever  = ZMQStream(self.recever)
          self.recever.on_recv(self.handle_from_broker)
          
          self.push = self._context.socket(zmq.PUSH)
          broker_back = url + str(data["worker_to_broker_back_port"])
          self.push.connect(broker_back)
          print "pull from broker" + front + "push to broker "+ broker_back

          #TODO sub implement

      def handle_from_broker(self,msg):
          
          parsed = json.loads(msg[0])
          
          #dispatch to module
          self._module.execute_work(parsed,self.push)

      def push_handle(self,msg):

          print "msg_broker %s" + msg
#          self._front_push.send_json(msg)

      def start(self):

          print "start"
          loop = IOLoop.current()
          loop.start()

