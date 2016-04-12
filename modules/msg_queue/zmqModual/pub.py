import zmq
import random
import sys
import time
import json

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = random.randrange(9999,10002)
    messagedata = random.randrange(1,215) - 80
    print "%d %d" % (topic, messagedata)
    #socket.send("%d %d" % (topic, messagedata))
    data = dict()
    data['msg']= messagedata   
    socket.send_multipart([str(topic),str(data)])
    time.sleep(1)
