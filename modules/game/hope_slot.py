import json

def handle(json_msg):
    print "hope_slot"
    print json_msg
    #return normal_handle(json_msg)
    return temp_handle(json_msg)

def temp_handle(json_msg):

    if json_msg['cmd'] == "request_join":
       rep = header(json_msg)
       rep['state'] = "game_join_ok"

       #TODO gamestart
#       res_json = http_query(json_msg['cmd'],name_pw[0],name_pw[1],-1)
       rep['init_info'] = "you get init"

#       rep['UserPoint'] =
       return rep

def normal_handle(json_msg):

    if json_msg['cmd'] == "request_join":
#    if json_msg['cmd'] == "request_open":
#       wait in backi( match algo),ready, open a game to service

       # get info from redis
       # 
       rep = header(json_msg)
       rep['state'] = "game_join_ok"

       #TODO gamestart
       rep['init_info'] = "you get init"
       return rep


def header(json_msg):

    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

