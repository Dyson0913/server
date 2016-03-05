from collections import *
import datetime


def handler(client,data):
    
    if data["message_type"] == "login":
         pass
#        print data['result']
        #client.write_message(msg)
 
def header(msg_type):
    header = OrderedDict()
    header["message_type"] = msg_type
    return header

       
