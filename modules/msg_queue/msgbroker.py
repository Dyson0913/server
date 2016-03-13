import zmq


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

    zmq.device(zmq.QUEUE, frontend, backend)
    print "broker start"
    # We never get here...
    frontend.close()
    backend.close()
    context.term()


def main():
    
    start_msgqueue(7788,8899)


if __name__ == "__main__":
    main()

