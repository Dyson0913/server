import zmq
import json

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop


import sys
#sys.path.append('../')

ioloop.install()


class zmq_msg_proxy(object):

      def __init__(self,data):

          self._domain = data["domain"]
          self._front_push_port = data["front_push_port"]
          self._front_pull_port = data["front_pull_port"]
          self._id = data["id"]

          self._context = zmq.Context()
          url = "tcp://"+self._domain + ":"

          #send from front 
          self.recever = self._context.socket(zmq.PULL)
          front = url + str(self._front_push_port)
          self.recever.connect(front)
          self.recever  = ZMQStream(self.recever)
          self.recever.on_recv(self.pull_handle)
          
          #send to front
          self._front_push = self._context.socket(zmq.PUSH)
          front_pull = url + str(self._front_pull_port)
          self._front_push.connect(front_pull)
          self._front_push  = ZMQStream(self._front_push)
          self._front_push.on_recv(self.push_handle)

          print "pull front " + front + "push to front " + front_pull

          #send to broker
          #data["pub_broker_port"]
          self.pub = self._context.socket(zmq.PUSH)
          pub = url + str(data["broker_front_port"])
          self.pub.connect(pub)
          
          print "pub to " +pub

      def pull_handle(self,msg):
          
          print "pull_handle"
          print msg
          parsed = json.loads(msg[0])
          #self.pub.send_multipart([str(self._id),str(msg)])
          self.pub.send_json(msg)

      def push_handle(self,msg):

          #del data just for db
          if 'for_db' in result:
              del result['for_db']
              del result['key']
                 
          #response to client
          print "msg_broker %s" + msg
#          self._front_push.send_json(msg)

      def start(self):

          print "start"
          loop = IOLoop.current()
          loop.start()
