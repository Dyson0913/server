import json

def init():
    print "fake init"

def p(json_msg):
    print "fake module"
    print json_msg
    return blocking_test(json_msg) 



def blocking_test(json_msg):

    rep = dict()

    if json_msg['id'] == 2:
       print "fake return"
    else:
       print "normal"
       rep['message_type'] = "login"
       rep['result'] = 0
       rep['client_id'] = json_msg['client_id']

    return rep
