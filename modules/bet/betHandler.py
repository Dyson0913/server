import json

_db = None

def handle(json_msg,socket_list):

    rep = normal_handle(json_msg,socket_list)

    if rep == None:
        return

    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    global _db
    _db = socket_list[1]

    print "bet_handler get cmd %s" % json_msg['cmd']

    rep = header(json_msg)
    if json_msg['cmd'] == "bet":
        uid = json_msg['uuid']
        game_id = json_msg['game_id']
        bet_info = json_msg['bet_info']

        result = query_bet(uid, game_id,bet_info)
        rep['state'] = "bet_ok"
        return rep

    if json_msg['cmd'] == "cancel_bet":
        pass


def header(json_msg):
    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

def query_bet(id, game_id,bet_info):
    #get acc from db
    global _db
    acc = _db.get(id)
    if acc != None:
        playerstate = get_info(acc)
        credit_info = playerstate['for_db']['playerinfo']['credit']

        #check crdit enough
        if game_id in credit_info:
            my_rest_credit = credit_info[game_id]

            #count new betlist can affordable
            for bet in bet_info:
                print bet['type']
                print bet['amount']
        return False
    else:
       # illegle acc ,return 0 point
        return False

def get_info(playerdata):
    return json.loads(playerdata)

def update_credit(id,credit,override = False):
    global _db
    acc = _db.get(id)
    if acc != None:
        playerstate = get_info(acc)
        if override == True :
            playerstate['for_db']['playerinfo']['credit'] = credit
        else:
            playerstate['for_db']['playerinfo']['credit'].update(credit)
        _db.update(playerstate) 
    else:
        # illegle acc ,no handle
        pass
