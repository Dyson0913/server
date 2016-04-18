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
          self._sub_mgr_port = data["sub_mgr_port"]

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

          print "front to " + front + " front_pull " + front_pull

          #send to msg broker dealer 
          self.pub = self._context.socket(zmq.PUB)
          pub = url + "7777"
          self.pub.connect(pub)
          
          print "pub to  " +pub 
          #recever from msg broker
#          self.sub= self._context.socket(zmq.SUB)
#          sub = url + "7788"
#          self.sub.connect(sub)
#          self.sub = ZMQStream(self.sub)
#          self.sub.on_recv(self.sub_handle)


          #sub from mgr
          #self._sub_from_mgr = self._context.socket(zmq.SUB)
          #sub_mgr = url + str(self._sub_mgr_port)
          #self._sub_from_mgr.connect (sub_mgr)
          #topicfilter = "9999"
          #self._sub_from_mgr.setsockopt(zmq.SUBSCRIBE, topicfilter)

      def pull_handle(self,msg):
          
          print "pull_handle"
          parsed = json.loads(msg[0])
          print parsed
          self.pub.send_multipart([str(1),str(msg)])
          #self.pub.send(msg)

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
#          while True:
#              json_msg = self.receiver.recv_json()
#              result = self._module.execute_work(json_msg) 
              
          #    string,jsonmsg = self._sub_from_mgr.recv_multipart()
          #    print string
          #    print jsonmsg

def main():
    worker = zmqWorker('localhost',8899)
    worker.start()

if __name__ == "__main__":

    main()

