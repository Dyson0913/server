import json

def handle(json_msg,socket_list):

    rep =  normal_handle(json_msg,socket_list)
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    db = socket_list[1]

    print "lobby get cmd %s" % json_msg['cmd']
   
    if json_msg['cmd'] == "request_gamelist":
       rep = header(json_msg)
       rep['state'] = "lobby_waitting"
       db.save(rep)

       gamelist_json_data = json.loads(db.get("gamelist"))
       rep['gamelist'] = gamelist_json_data["app"]

       return rep


def header(json_msg):

    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

