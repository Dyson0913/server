import sys
import zmq

#from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)



# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from weather server..."
socket.connect ("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

# Subscribe to zipcode, default is NYC, 10001
topicfilter = "9999"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

#pub 2 ,after down work,repoert to sub2
url = "tcp://localhost:"+"9990"
pub2 = context.socket(zmq.PUB)
pub2.connect(url)
print "pub2 in " + url



# Process 5 updates
total_value = 0
for update_nbr in range (5):
    #string = socket.recv()
    string,jsonmsg = socket.recv_multipart()
    print string
    print jsonmsg
    pub2.send_multipart([str(string),str(jsonmsg)])

#    topic, messagedata = string.split()
#    print topic, messagedata

print "Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr)
