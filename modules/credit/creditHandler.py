import json

_db = None

def handle(json_msg,socket_list):

    rep = normal_handle(json_msg,socket_list)
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    global _db
    _db = socket_list[1]

    print "credit get cmd %s" % json_msg['cmd']
   
    if json_msg['cmd'] == "takein":
       rep = header(json_msg)
       rep['state'] = "userCredit_update"
       rep['total_Credit'] = key_check(json_msg['uuid'])
       return rep


def header(json_msg):
    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

def key_check(id):
    #get acc from db
    global _db
    acc = _db.get(id)
    if acc != None:
        playerstate = get_info(acc)
        credit_info = playerstate['for_db']['playerinfo']['credit']
        return credit_info['total']
    else:
       # illegle acc ,return 0 point
        return 0


def get_info(playerdata):
    return json.loads(playerdata)
