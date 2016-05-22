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
          self._proxy_push_port = data["proxy_push_port"]
          self._proxy_pull_port = data["proxy_pull_port"]
          self._id = data["id"]

          self._uniq_id = None

          self._context = zmq.Context()
          url = "tcp://"+self._domain + ":"

          #send from front 
          self.recever = self._context.socket(zmq.PULL)
          front = url + str(self._proxy_push_port)
          self.recever.connect(front)
          self.recever  = ZMQStream(self.recever)
          self.recever.on_recv(self.pull_handle)
          
          #send to front
          self._front_push = self._context.socket(zmq.PUSH)
          front_pull = url + str(self._proxy_pull_port)
          self._front_push.connect(front_pull)
          #self._front_push  = ZMQStream(self._front_push)
          #self._front_push.on_recv(self.push_handle)

          print "pull front " + front + "push to front " + front_pull

          #send to broker
          #data["pub_broker_port"]
          self.broker_push = self._context.socket(zmq.PUSH)
          push = url + str(data["broker_to_worker_front_port"])
          self.broker_push.connect(push)
          
          self.broker_pull = self._context.socket(zmq.PULL)
          pull = url + str(data["worker_to_broker_front_port"])
          self.broker_pull.connect(pull)
          self.broker  = ZMQStream(self.broker_pull)
          self.broker.on_recv(self.push_handle)
          print "push to " + push + "pull from " + pull

      def pull_handle(self,msg):
          
          parsed = json.loads(msg[0])
          parsed['proxy_id'] = self._uniq_id
          #self.pub.send_multipart([str(self._id),str(msg)])
          
          if 'trans' in parsed:
               print "get trans info wait"
               #TODO pass close game to worker
               return

          self.broker_push.send_json(parsed)

      def push_handle(self,msg):

          result = json.loads(msg[0])
          #print result

          #pass data to another module
          if 'module' in result:
              print "worker msg , pass back"
              self.broker_push.send_json(result)

              return

          #del data just for db
          if 'for_db' in result:
              del result['for_db']
              del result['key']
              if 'proxy_id' in result:
                  del result['proxy_id']
                 
          #response to client
          self._front_push.send_json(result)

      def set_identity(self,uniq_id):
          self._uniq_id = uniq_id

      def start(self):

          print "%s start!!" % self._uniq_id
          loop = IOLoop.current()
          loop.start()
