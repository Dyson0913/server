from protocol import*
from collections import *
import logging
import datetime

time = datetime.datetime.now()


def chat_handler(client,data,count):
    
    if count == 0:
        show_time(client,count,"first") 
    if count  == (client.totalClient-1):
        client.set_time() 
        show_time(client,count,"talk") 
        
        
def show_time(client,count,state):
    if count  == 0:
        global time 
        time = datetime.datetime.now()
        #print state
        #print "zero {0} = {1}".format(count,time)
    if count  == (client.totalClient-1):
        client.set_time()
         
        global time 
        #print state
        #print "time {0}".format(client.time)
        client.show_time( time)
        #print "end {0} = {1}".format(count,time)
      
 
def header(msg_type):
    header = OrderedDict()
    header["message_type"] = msg_type
    return header

       
