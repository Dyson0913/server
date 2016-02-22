from websocket import create_connection
import websocket
import datetime
from di import *
import json
import chat_handler
import thread

class Client(object):

    def __init__(self):
#        print "client init"
        self.socket = None;
        self.time_now = datetime.datetime.now()
        self.time_out = datetime.timedelta(seconds=1)
        self.totalClient = 0
        self.time = datetime.datetime.now()
        self.connect = True

    def creat_ws(self,url,num):
        self.socket = create_connection(url)
        self.totalClient = num

    def on_message(self,count):
        #if datetime.datetime.now() - self.time_now >self.time_out:
            #self.time_now = datetime.datetime.now()
            
            result = self.socket.recv()
            #print "receiv %s" % result
            parse = json.loads(result)
            self.parse.chat_handler(self,parse,count)

    def on_close(self):
        self.socket.close()

    def show_time(self,time):
        print self.time - time

    def set_time(self):
        self.time =  datetime.datetime.now()

    def write_message(self,message):
        json_string = json.dumps(message)
        self.socket.send(json_string)

class ClientMgr(object):
    
    def __init__(self,url):
#        print "Clientmgr init"
        self.client = []
        self.url = url
        self.clientNum = 0
        self.connect = True

    def create_user(self,num):
        self.clientNum = num
        for i in range(num):
            myclient = inject(Client(),parse = chat_handler)
            myclient.creat_ws(self.url,num)
            self.client.append(myclient)
            print i

    def check_user(self):
        for i in range(self.clientNum):            
            self.client[i].on_message(i)
        

       
    def close_user(self):
        for i in range(self.clientNum):
            self.client[i].on_close()

def main():
    
    clientMgr = ClientMgr('ws://106.186.116.216:8888/chatsocket')
    clientMgr.create_user(1)

    while clientMgr.connect:
        clientMgr.check_user()
    
    clientMgr.close_user()
    

if __name__ == "__main__":
    main()

