import zmq
from config_parser import *


def start_msgqueue(frontend_port, backend_port):

    context = zmq.Context()

    # Socket facing clients
    frontend = context.socket(zmq.ROUTER)
    frontend_addr = "tcp://*:%d" % frontend_port
    frontend.bind(frontend_addr)
    print "router"
    # Socket facing services
    backend  = context.socket(zmq.DEALER)
    backend_addr = "tcp://*:%d" % backend_port
    backend.bind(backend_addr)

    print "dealer"
    #for res/rep
    zmq.device(zmq.QUEUE, frontend, backend)

    #for pub/sub
    #zmq.device(zmq.FORWARDER, frontend, backend)

    #for pipelind
    #zmq.device(zmq.STREAMER, frontend, backend)

    print "broker start"
    # We never get here...
    frontend.close()
    backend.close()
    context.term()


def start_pub_sub_proxy(sub_port, pub_port):

    context = zmq.Context()

    sub = context.socket(zmq.XSUB)
    sub_addr = "tcp://*:%d" % sub_port
    sub.bind(sub_addr)

    pub = context.socket(zmq.XPUB)
    pub_addr = "tcp://*:%d" % pub_port
    pub.bind(pub_addr)

    zmq.proxy(pub,sub,None)

def main():

    data = config_parser()
    
    #start_msgqueue(7777,8888)
    start_pub_sub_proxy(data["sub_broker_port"],data["pub_broker_port"])


if __name__ == "__main__":
    main()

