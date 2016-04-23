import json

def handle(json_msg):
    print json_msg
#    return normal_handle(json_msg) 
    return blocking_test(json_msg) 

def normal_handle(json_msg):

    if json_msg['cmd'] == "login":
       #always return ok
       rep = header(json_msg)
       rep['state'] = "login_ok"
       rep['uuid'] = json_msg['client_id']
       return rep

    if json_msg['cmd'] == "self_close":
       rep = header(json_msg)
       rep['state'] = "self_close"
       return rep

def blocking_test(json_msg):

    if json_msg['id'] == 2:
       print "fake return"
    else:
       print "normal"
       rep = header(json_msg)
       rep['state'] = "login_ok"
       return rep

def header(json_msg):

    rep = dict()
    rep['client_id'] = json_msg['client_id']
    return rep 
