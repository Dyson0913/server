import json

def handle(json_msg,socket_list):
    print json_msg
    rep = normal_handle(json_msg) 
#    rep = blocking_test(json_msg)
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg):

    if json_msg['cmd'] == "login":
       name_pw = "test2_test2".split("_")
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
           rep['key'] = name_pw[0]

       else:
           rep['state'] = "login_fail"
           rep['reason'] = "no_such_account"
       rep['uuid'] = name_pw[0]
       return rep

    if json_msg['cmd'] == "self_close":

       #TODO get player now where
       rep = header(json_msg)
       rep['state'] = "self_close"
       return rep

def fake_login():
    rep = dict()
    rep['result'] = 1
    return rep

def fake_playerinfo():
    rep = dict()
    rep['result'] = 1000
    return rep

def blocking_test(json_msg):

    if json_msg['id'] == 2:
       print "fake return"
    else:
       print "normal"
       rep = header(json_msg)
       rep['state'] = "login_ok"
       rep['uuid'] = "fake_tester" 
       return rep

def header(json_msg):

    rep = dict()
    rep['client_id'] = json_msg['client_id']
    rep['cmd'] = json_msg['cmd']
    rep['key'] = rep['client_id']

    return rep
