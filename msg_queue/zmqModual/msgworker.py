import zmq
import json
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


class zmqWorker(object):

      def __init__(self,data):

          self._domain = data["domain"]
          self._front_port = data["front_port"]
          self._back_port = data["back_port"]

          self._context = zmq.Context()
#          self.linger = 0
          url = "tcp://"+self._domain + ":" + str(self._front_port)
          print "link front to " + url

          #send Front 
          self.receiver = self._context.socket(zmq.PULL)
          self.receiver.connect(url)

          back_url = "tcp://"+self._domain + ":" + str(self._back_port)
          print "link back to " + back_url

          #push to back & front
          self._send = self._context.socket(zmq.PUSH)
          self._send.connect(back_url)


      def start(self):

          print "start"
          while True:
              work = self.receiver.recv_json()
              self.blocking_test(work);


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
          
      def blocking_test(self,work):
          if work['id'] == 2:
              self._send.send_json(work)
              print "fake return"
          else:
              print "normal"
              self._send.send_json(work)
        

def main():
    worker = zmqWorker('localhost',8899)
    worker.start()

if __name__ == "__main__":

    main()

