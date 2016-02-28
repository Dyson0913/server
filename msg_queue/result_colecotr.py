import time
import zmq
import pprint

def result_collector(domain,port_to_front):

    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    url = "tcp://"+ domain + ":" + str(port_to_front)
    print "listen port " +url 
    results_receiver.bind(url)
    collecter_data = {}
    while (True):
    
        result = results_receiver.recv_json()
        pprint.pprint(result)


def main():
    reslut = result_collector("*",6669)
   

if __name__ == "__main__":
    main() 
