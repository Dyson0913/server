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
          self.broker_push = self._context.socket(zmq.PUSH)
          push = url + str(data["broker_to_worker_front_port"])
          self.broker_push.connect(push)
          
          self.broker_pull = self._context.socket(zmq.PULL)
          pull = url + str(data["worker_to_broker_front_port"])
          self.broker_pull.connect(pull)
          self.broker  = ZMQStream(self.broker_pull)
          self.broker.on_recv(self.push_handle)
          print "push to " + push + "pull from " + pull

          #sub from request
          self.sub = self._context.socket(zmq.SUB)
          sub = url + str(data["proxy_pub_port"])
          self.sub.connect(sub)

          #pub to worker
          bind_url = "tcp://*:"
          self.pub_to_worker = self._context.socket(zmq.PUB)
          pub_url = bind_url + str(data["worker_pub_port"])
          self.pub_to_worker.bind(pub_url)

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
#          print result

          #pass data to another module
          if 'module' in result:
              print "worker pass msg , pass back(auth close)"
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

          #ip & os id ,just save ip
          ip_osid = uniq_id.split("_")
          #using ip for uniq id
          self._uniq_id = ip_osid[0]
          
          topic_filter = "1" #self._uniq_id
          self.sub.setsockopt(zmq.SUBSCRIBE, topic_filter)
          self.sub  = ZMQStream(self.sub)
          self.sub.on_recv(self.sub_handle)

      def sub_handle(self,msg):
          print "sub handle"
          print msg

      def start(self):

          print "%s start!!" % self._uniq_id
          loop = IOLoop.current()
          loop.start()
