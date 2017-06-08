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
        if result == True:
            rep['state'] = "bet_ok"
        else:
            rep['state'] = "bet_fail"
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
    global _db
    acc = _db.get(id)
    if acc != None:
        playerstate = get_info(acc)
        credit_info = playerstate['for_db']['playerinfo']['credit']
        #check crdit enough
        if game_id in credit_info:
            my_rest_credit = credit_info[game_id]
            
            #count new betlist can affordable
            bet_total = 0
            for bet in bet_info:
                rep = dict()
                bet_total += bet['amount']
 
            if my_rest_credit > bet_total:
               my_rest_credit -= bet_total
               credit_info[game_id] = my_rest_credit
               playerstate['for_db']['playerinfo']['credit'] = credit_info

               #saving bill
               if 'bill' in playerstate['for_db']:
                   playerstate['for_db']['bill']['bet'].extend(bet_info)
               else:
                   new_json = dict()
                   new_json['game_id'] = game_id
                   new_json['bet'] = bet_info
                   playerstate['for_db']['bill'] = new_json
               _db.update(playerstate)
               return True
        return False
    else:
       # illegle acc ,return 0 point
        return False

def get_info(playerdata):
    return json.loads(playerdata)

