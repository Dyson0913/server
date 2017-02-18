import json
import hashlib

def handle(json_msg,socket_list):
    #print json_msg
    rep = normal_handle(json_msg,socket_list)
#    rep = blocking_test(json_msg)
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    db = socket_list[1]

    print "auth get cmd %s" % json_msg['cmd']

    if json_msg['cmd'] == "login":
       name_pw = json_msg["token"].split("_")
       #name_pw = "test2_test2".split("_")
       res_json = fake_login()
       rep = header(json_msg)
       if res_json['result'] == 1:
           rep['state'] = "login_ok"
           playerinfo_json = fake_playerinfo()
           playerinfo = dict()
           playerinfo['credit'] = playerinfo_json['result']
           playerinfo['name'] = name_pw[0]
           playerinfo['pw'] = name_pw[1]

           msg = dict()
           msg['playerinfo'] = playerinfo
           rep['for_db'] = msg
           rep['key'] = token(json_msg["token"])
           db.save(rep)
       else:
           rep['state'] = "login_fail"
           rep['reason'] = "no_such_account"
       rep['uuid'] = rep['key']
       return rep

    if json_msg['cmd'] == "self_close":

       #TODO get player now where ,notify game close
       playerstate = json.loads(db.get(json_msg['uuid']))
       info = playerstate['state']

       #notify game close self
       #TODO versus leave group
       if info != "lobby_waitting":
            to_game = header_for_close(json_msg)
            to_game['module'] = playerstate['playing_module']
            to_game['game_id'] = playerstate['playing_group']
            to_game['cmd'] = "leave_game"
            player_socket.send_json(to_game)    
         

       rep = header_for_close(json_msg)
       rep['state'] = "self_close"

       db.save(rep)


       return rep

def fake_login():
    rep = dict()
    rep['result'] = 1
    return rep

def fake_playerinfo():
    rep = dict()
    rep['result'] = 1000
    return rep

def header_for_close(json_msg):

    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['cmd'] = json_msg['cmd']
    rep['key'] = json_msg['uuid']
    return rep

def header(json_msg):
    rep = dict()
    rep['client_id'] = json_msg['client_id']
    rep['cmd'] = json_msg['cmd']
    rep['key'] = rep['client_id']
    return rep

def token(name):
    sha1 = hashlib.sha1()
    data = name
    sha1.update(data.encode('utf-8'))
    sha1_data = sha1.hexdigest()
    print(sha1_data)
    return sha1_data
