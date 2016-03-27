import sys
sys.path.append('../')

from httpquery import *

def handle(json_msg):
    print "hojo_auth"
    print json_msg
    return normal_handle(json_msg) 

def normal_handle(json_msg):

    if json_msg['cmd'] == "login":
       name_pw = json_msg["token"].split("_")
       res_json = http_query(json_msg['cmd'],name_pw[0],name_pw[1],-1)
       rep = header(json_msg)
       if res_json['result'] == "1":
           rep['state'] = "login_ok"
           playerinfo_json = http_query('get_credit',name_pw[0],name_pw[1],-1)
           playerinfo = dict()
           playerinfo['name'] = name_pw[0]
           playerinfo['pw'] = name_pw[1]
           playerinfo['credit'] = playerinfo_json['result']

           msg = dict()
           msg['playerinfo'] = playerinfo
           rep['for_db'] = msg
           rep['key'] = name_pw[0]

       else:
           rep['state'] = "login_fail"
           res['reason'] = "no_such_account"
       rep['uuid'] = name_pw[0] #json_msg['client_id']
       return rep

    if json_msg['cmd'] == "self_close":
       rep = header(json_msg)
       rep['state'] = "self_close"
       return rep


def header(json_msg):

    rep = dict()
    rep['client_id'] = json_msg['client_id']
    rep['cmd'] = json_msg['cmd']
    rep['key'] = rep['client_id']

    return rep 
