import json

def handle(json_msg):
    print json_msg
    return normal_handle(json_msg)
#    return blocking_test(json_msg)

def normal_handle(json_msg):

    if json_msg['cmd'] == "request_gamelist":
       rep = header(json_msg)
       rep['state'] = "lobby_waitting"

       #TODO gamelist get
       rep['gamelist'] = "baccarat"
       return rep


def header(json_msg):

    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

