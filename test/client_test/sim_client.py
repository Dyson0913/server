from websocket import create_connection
import datetime
from di import *
import json
from login_handler import *
import multiprocessing

import websocket
from datetime import timedelta
import time

import tornado.options
from tornado.options import define,options

define("num", default=2, help="run num on the given", type=int)
define("core", default=10, help="run num on the given", type=int)
define("port", default=7000, help="run on the given port", type=int)


class Client(object):

    def __init__(self,mgr):
        self.socket = None;
        self._mgr = mgr
        self.totalClient = 0
        self.core_id = None
        self.time = datetime.datetime.now()
        self._delta_time = 0;
        self.connect = False

    def creat_ws(self):
        #low leval connect
        self.socket = create_connection(self.url)
        self.set_time()
    
    def on_message(self):
 
        if self.connect == False:
           self.connect = True
        #print "core "+ str(self.core_id)+" client = "+ str(self.totalClient) + " on_message"
        result = self.socket.recv()
        #print result
        #count time
        #self._mgr.info_colle(self.delta_time())

        parse = json.loads(result)
        self.parse(self,parse)
        print self.delta_time()

    def delta_time(self):
        self._delta_time = datetime.datetime.now() - self.time
        return self._delta_time

    def set_time(self):
        self.time =  datetime.datetime.now()

    def write_message(self,message):
        json_string = json.dumps(message)
        self.socket.send(json_string)

class ClientMgr(object):
    
    def __init__(self,url):
        self.client = []
        self.url = url
        self.clientNum = 0
        self.cnt = 0
        self.connect = True
        self.core_id = None
        self.total_time = datetime.timedelta(microseconds=0);

    def create_user(self,num,core_id):
        self.clientNum = num
        self.core_id = core_id
        for i in range(num):
            myclient = inject(Client(self),parse = handler)
            myclient.url = self.url
            myclient.core_id = core_id
            myclient.totalClient = i
            myclient.creat_ws()
            #time.sleep(0.5)
            self.client.append(myclient)

    def info_colle(self,report_info):
        self.total_time += report_info
        self.cnt +=1
        if self.clientNum == self.cnt:
            print self.total_time

    def check_user(self):
        for i in range(self.clientNum):            
            self.client[i].on_message()
       
    def close_user(self):
        for i in range(self.clientNum):
            self.client[i].on_close()

def process(port):

    for i in range(options.core):
        #print "processing {0}".format(i)
        p = multiprocessing.Process(target=check,args=(str(i),port))
        p.start()

def thread_():
    
    thread.start_new_thread(check,("thread-1",1))
    time.sleep(1)

def check(core_id,port):
    clientMgr = ClientMgr('ws://108.61.246.195:'+str(port)+'/gamesocket/1')
    #clientMgr = ClientMgr('ws://106.186.116.216:7000/gamesocket/1')
    clientMgr.create_user(options.num,core_id)

    while(True):
        clientMgr.check_user()

def main():
   
    tornado.options.parse_command_line() 
    websocket.enableTrace(False)

#    thread_()
    process(options.port) 

if __name__ == "__main__":
    main()

