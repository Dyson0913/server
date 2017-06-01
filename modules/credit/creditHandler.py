import json

_db = None

def handle(json_msg,socket_list):

    rep = normal_handle(json_msg,socket_list)
    print rep
    socket = socket_list[0]
    socket.send_json(rep)

def normal_handle(json_msg,socket_list):

    global _db
    _db = socket_list[1]

    print "credit get cmd %s" % json_msg['cmd']

    rep = header(json_msg)
    if json_msg['cmd'] == "query_credit":

        rep['state'] = "userCredit_update"
        rep['total_Credit'] = query_point(json_msg['uuid'], "total")
        return rep

    if json_msg['cmd'] == "take_in":
        mycredit = query_point(json_msg['uuid'], "total")
        takein = json_msg['takein_credit']
        if takein > mycredit:
            rep['state'] = "takein_result"
            rep['result'] = "fail"
            rep['reason'] = "credit not enough"
        else:
            new_credit = dict()
            new_credit['total'] = mycredit - takein
            new_credit[json_msg['game']] = takein
            update_credit(json_msg['uuid'],new_credit)

            rep['state'] = "takein_result"
            rep['result'] = "ok"
        return rep

    if json_msg['cmd'] == "return_point_from_game":
        mycredit = query_point(json_msg['uuid'], "total")
        game_credit = query_point(json_msg['uuid'], json_msg['game_serial'])

        new_credit = dict()
        new_credit['total'] = mycredit + game_credit
        update_credit(json_msg['uuid'], new_credit,True)

        rep['module'] = "lobby"
        rep['cmd'] = "request_gamelist"
        return rep


def header(json_msg):
    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

def query_point(id, field):
    #get acc from db
    global _db
    acc = _db.get(id)
    if acc != None:
        playerstate = get_info(acc)
        credit_info = playerstate['for_db']['playerinfo']['credit']
        if field in credit_info:
            return credit_info[field]
        return 0
    else:
       # illegle acc ,return 0 point
        return 0

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
