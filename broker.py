import zmq
from config_parser import *

def start_msgqueue(frontend_port, backend_port):

    context = zmq.Context()

    # Socket facing clients
    frontend = context.socket(zmq.ROUTER)
    frontend_addr = "tcp://*:%d" % frontend_port
    frontend.bind(frontend_addr)

    # Socket facing services
    backend  = context.socket(zmq.DEALER)
    backend_addr = "tcp://*:%d" % backend_port
    backend.bind(backend_addr)

    print "router/dealer"
    #for res/rep
    zmq.device(zmq.QUEUE, frontend, backend)

    print "broker start"
    # We never get here...
    frontend.close()
    backend.close()
    context.term()


def start_pub_sub_proxy(front_port, back_port):

    context = zmq.Context()

    sub = context.socket(zmq.XSUB)
    sub_addr = "tcp://*:%d" % front_port
    sub.bind(sub_addr)

    pub = context.socket(zmq.XPUB)
    pub_addr = "tcp://*:%d" % back_port
    pub.bind(pub_addr)

    zmq.proxy(pub,sub,None)

    #for pub/sub
    #zmq.device(zmq.FORWARDER, frontend, backend)

def start_push_pull(frontend_port, backend_port):

    context = zmq.Context()

    # Socket facing clients
    frontend = context.socket(zmq.PULL)
    frontend_addr = "tcp://*:%d" % frontend_port
    frontend.bind(frontend_addr)

    # Socket facing services
    backend  = context.socket(zmq.PUSH)
    back_addr = "tcp://*:%d" % backend_port
    backend.bind(back_addr)

    print "push/pull"

    #for push/pull
    zmq.device(zmq.STREAMER, frontend, backend)

def main():

    data = config_parser()
    start_push_pull(data["broker_front_port"],data["broker_back_port"])
    #start_msgqueue(data["broker_front_port"],data["broker_back_port"])
    #start_pub_sub_proxy(data["broker_front_port"],data["pub_broker_port"])


if __name__ == "__main__":
    main()

