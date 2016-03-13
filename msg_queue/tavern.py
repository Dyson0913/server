import zmq

import sys
sys.path.append("../modules/db")
sys.path.append("../modules/db/noSQL")


from db_proxy import *
from config_parser import *

class tavern(object):

    def __init__(self,data):
        port_from_worker = data["back_port"]
        domain = "*"

        self.context = zmq.Context()
        self._receiver = self.context.socket(zmq.PULL)
        url = "tcp://"+ domain + ":" + str(port_from_worker)
        print "listen port " +url
        self._receiver.bind(url)

        db_host = data['db']['host']
        db_port = data['db']['port']
        db_pw = data['dbpw']
        self._db = db_proxy(db_host,db_port,db_pw)

    def handle(self,json_msg):
        print "tavern handle %s " % json_msg 
        if json_msg['state'] == "log_out":
            self._db.clean(json_msg['client_id'])
            return

        self._db.save(json_msg)

    def Receive(self):
        while True:
            result = self._receiver.recv_json()
            self.handle(result)

def main():
    data = config_parser()
    mytravern = tavern(data)

    mytravern.Receive()   

if __name__ == "__main__":
    main() 
