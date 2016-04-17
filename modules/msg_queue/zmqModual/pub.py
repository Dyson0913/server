import zmq
import random
import sys
import time
import json

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop


ioloop.install()


def hand(msg):
    #parsed = json.loads(msg[0])
    parsed = msg
    print "pub hand"
    print parsed


port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

url = "tcp://*:"+"9990"

receiver = context.socket(zmq.SUB)
receiver.bind(url)
print "sub in " +url
topicfilter = "9999"
receiver.setsockopt(zmq.SUBSCRIBE, topicfilter)


receiver  = ZMQStream(receiver)
receiver.on_recv(hand)
#loop = IOLoop.current()
#loop.start()


while True:
    topic = random.randrange(9999,10002)
    messagedata = random.randrange(1,215) - 80
    print "%d %d" % (topic, messagedata)
    #socket.send("%d %d" % (topic, messagedata))
    data = dict()
    data['msg']= messagedata   
    socket.send_multipart([str(topic),str(data)])
    time.sleep(1)
