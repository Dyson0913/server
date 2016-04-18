import zmq
import json

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop


import sys
#sys.path.append('../../../')

ioloop.install()


class msgworker(object):

      def __init__(self,data):

          self._domain = data["domain"]
          self._front_push_port = data["front_push_port"]
          self._front_pull_port = data["front_pull_port"]

          self._context = zmq.Context()
          url = "tcp://"+self._domain + ":"

          #send from front 
          self.recever = self._context.socket(zmq.SUB)
          front = url + str("8888")
          topicfilter = "1"
          self.recever.setsockopt(zmq.SUBSCRIBE, topicfilter)
          self.recever.connect(front)
#          self.recever.bind("tcp://*:"+"8899")
          
          self.recever  = ZMQStream(self.recever)
          self.recever.on_recv(self.sub_handle)
          print "sub from " + front

          #sub_mgr = url + str(self._sub_mgr_port)
          #self._sub_from_mgr.connect (sub_mgr)
          #topicfilter = "9999"
          #self._sub_from_mgr.setsockopt(zmq.SUBSCRIBE, topicfilter)

      def sub_handle(self,msg):
          
          print "sub_handle"
          #parsed = json.loads(msg[0])
          print msg
          ##self.pub.send_multipart([str("1"),str(msg)])


      def push_handle(self,msg):

          print "msg_broker %s" + msg
#          self._front_push.send_json(msg)

      def start(self):

          print "start"
          loop = IOLoop.current()
          loop.start()

