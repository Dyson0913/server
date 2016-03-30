import json

from baccarat_mgr import *



def handle(json_msg):
    print "baccarat handle"
    print json_msg
    return normal_handle(json_msg)

def normal_handle(json_msg):



def header(json_msg):

    rep = dict()
    rep['client_id'] = json_msg['client_id']
    return rep

