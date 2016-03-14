import json

def handle(json_msg):
    print json_msg
    return normal_handle(json_msg)
#    return blocking_test(json_msg)

def normal_handle(json_msg):

    if json_msg['cmd'] == "request_join":
       rep = header(json_msg)
       rep['state'] = "game_join_ok"

       #TODO gamestart
       rep['init_info'] = "you get init"
       return rep


def header(json_msg):

    rep = dict()
    rep['client_id'] = json_msg['client_id']
    return rep

