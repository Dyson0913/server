import zmq
import random
import sys
import time
import json

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

def hand(msg):
    #parsed = json.loads(msg[0])
    parsed = msg
    print "pub hand"
    print parsed


url = "tcp://*:"+"9990"
context = zmq.Context()
receiver = context.socket(zmq.SUB)
#receiver.bind(url)
receiver.bind(url)
print "sub in " +url
topicfilter = "9999"
receiver.setsockopt(zmq.SUBSCRIBE, topicfilter)


receiver  = ZMQStream(receiver)
receiver.on_recv(hand)

loop = IOLoop.current()
loop.start()
#ioloop.IOloop.instance().start()

#while True:
#    topic,jsonmsg = receiver.recv_multipart()
#    print "%s %s" % (topic, jsonmsg)
#time.sleep(1)
