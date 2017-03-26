import json
import hashlib

def handle(json_msg,socket_list):
    rep = normal_handle(json_msg,socket_list)
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    db = socket_list[1]

    print "auth get cmd %s" % json_msg['cmd']

    if json_msg['cmd'] == "try_login":
       return get_account(json_msg)
    if json_msg['cmd'] == "login":
       return get_account(json_msg)

    #close whole windows but network is still working,so can send message to auth
    if json_msg['cmd'] == "self_close":

       #TODO get player now where ,notify game close
       playerdata = db.get(json_msg['uuid'])
       #create account fail,just close socket 
       if playerdata == None:
           rep = header_for_close(json_msg)
           return rep

       playerstate = json.loads(playerdata)
       info = playerstate['state']

       #in game,pass msg to msg_proxy to notify game close self then update state
       #not in game,just update state
       #TODO versus leave group
       rep = header_for_close(json_msg)
       if info != "lobby_waitting":
           rep['module'] = playerstate['playing_module']
           rep['game_id'] = playerstate['playing_group']
           rep['cmd'] = "lost_connect"
       else:
           rep['state'] = "self_close"
           db.save(rep)


       return rep

def fake_login():
    rep = dict()
    rep['result'] = 0
    return rep

def fake_playerinfo():
    rep = dict()
    rep['result'] = 1000
    return rep

def get_account(json_msg):
    name_pw = json_msg["token"].split("_")
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
        rep['key'] = name_pw[0] #token(json_msg["token"])
        db.save(rep)
        rep['uuid'] = rep['key']
    else:
        rep['state'] = "login_fail"
        rep['reason'] = "no_such_account"
        rep['for_db'] = "for_del_key"
        rep['key'] = name_pw[0] #token(json_msg["token"])
        rep['uuid'] = rep['client_id']
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
