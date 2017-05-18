import json
import hashlib
import datetime

_db = None

def handle(json_msg,socket_list):
    rep = normal_handle(json_msg,socket_list)
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    global _db
    _db = socket_list[1]

    print "auth get cmd " + str(json_msg)

    if json_msg['cmd'] == "try_login":
       return get_account(json_msg)
    if json_msg['cmd'] == "login":
       return get_account(json_msg)

    #close whole windows but network is still working,so can send message to auth
    if json_msg['cmd'] == "self_close":

       #TODO get player now where ,notify game close
       playerdata = _db.get(json_msg['uuid'])
       #create account fail,just close socket 
       if playerdata == None:
           rep = header_for_close(json_msg)
           return rep

       playerstate = get_info(playerdata)

       #in game,pass msg to msg_proxy to notify game close self then update state
       #not in game,just update state
       #TODO versus leave group
       rep = header_for_close(json_msg)
       if playerstate['state'] != "lobby_waitting":
           rep['module'] = playerstate['playing_module']
           rep['game_id'] = playerstate['playing_group']
           rep['cmd'] = "lost_connect"
       else:
           rep['state'] = "self_close"
           _db.save(rep)


       return rep

def fake_login(id):
    #get acc from db
    global _db
    acc = _db.get(id[0])
    rep = dict()
    if acc != None:
        #check multi login
        playerstate = get_info(acc)
        #pw not equal,1.self forget 2,someone try pw
        if playerstate['for_db']['playerinfo']['pw'] != id[1]: 
            rep['result'] = 0
            rep['reason'] = "password error"
        else:
            #pw ok ,check is multi login by other socket
            if playerstate['state'] != "self_close":
                rep['result'] = 0
                rep['reason'] = "alreay login on other device!"
            else:
                rep['result'] = 1
    else:
        rep['result'] = 1
    return rep

def get_info(playerdata):
    return json.loads(playerdata)

def fake_playerinfo():
    rep = dict()
    rep['result'] = 1000
    return rep

def get_account(json_msg):
    name_pw = json_msg["token"].split("_")
    res_json = fake_login(name_pw)
    rep = header(json_msg)

    global _db

    point = get_info(_db.get("TryPoint"))
    if res_json['result'] == 1:
        rep['state'] = "login_ok"
        playerinfo = dict()
        playerinfo['credit'] = {'total':point['Freepoint']}
        playerinfo['name'] = name_pw[0]
        playerinfo['pw'] = name_pw[1]
        playerinfo['lastlogin'] = str(datetime.datetime.utcnow())

        msg = dict()
        msg['playerinfo'] = playerinfo
        rep['for_db'] = msg
        rep['key'] = name_pw[0] #token(json_msg["token"])
        _db.save(rep)
        rep['uuid'] = rep['key']
    else:
        rep['state'] = "login_fail"
        rep['reason'] = res_json['reason']
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
