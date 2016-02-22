import zmq
#from zmq.eventloop.zmqstream import ZMQStream

class zmqWorker(object):

      def __init__(self,domain,port):

          self._context = zmq.Context()
          self._socket = self._context.socket(zmq.REP)
#          self.linger = 0
          print "link to "+domain + " "+ str(port)
          self._socket.connect("tcp://" + domain + ":" + str(port) )

      def receive(self):

          msg = self._socket.recv_json()
          #msg = self._socket.recv()
          print "reciev %s" % msg

          #receive handle
          if msg['cmd'] == "login":
              rep = dict()
              rep['message_type'] = "login"
              rep['result'] = 0
              rep['client_id'] = msg['client_id']
              self._socket.send_json(rep)
          
          if msg['cmd'] == "close":
              #remnove sockmgr
          print rep
          


def main():
    worker = zmqWorker(localhost,8899)
    worker.receiver

if __name__ == "__main__":

    main()

