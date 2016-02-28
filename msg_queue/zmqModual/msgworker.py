import zmq
import json
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


class zmqWorker(object):

      def __init__(self,domain,port):

          self._context = zmq.Context()
          self._socket = self._context.socket(zmq.REP)
#          self.linger = 0
          print "link to "+domain + " "+ str(port)
          self._socket.connect("tcp://" + domain + ":" + str(port) )
          self.loop = IOLoop.instance()

      def start(self):

          stream = ZMQStream(self._socket)
          stream.on_recv(self.receive)
          self.loop.start()
          print "start"

      def receive(self,msg):
          msg = json.loads(msg[0])
#          msg = self._socket.recv_json()
          print "reciev %s" % msg

          #receive handle
          if msg['cmd'] == "login":
              if msg['id'] == 2:
                  print "get 1 no re"
                  return
              rep = dict()
              rep['message_type'] = "login"
              rep['result'] = 0
              rep['client_id'] = msg['client_id']
              self._socket.send_json(rep)
          
          if msg['cmd'] == "close":
              pass
          print rep
          


def main():
    worker = zmqWorker('localhost',8899)
    worker.start()

if __name__ == "__main__":

    main()

