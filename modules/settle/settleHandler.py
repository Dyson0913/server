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

    print "settle_handler get cmd %s" % json_msg['cmd']

    #rep = header(json_msg)
    if json_msg['cmd'] == "settle":
        game_id = json_msg['game_id']
        player_id = json_msg['settle_player_id']
        win_state = json_msg['game_result']
        for playerid in player_id:
            query_settle(playerid,game_id,win_state)


def query_settle(id, game_id, win_state):
    global _db
    acc = _db.get(id)
    if acc != None:
        playerstate = get_info(acc)
        if 'bill' in playerstate['for_db']:

            bill_info = playerstate['for_db']['bill']['bet']
            #settle crdit
            total_winlose = 0
            for bet in bill_info:
                total_winlose += win_state[bet['type']] * bet['amount']

            #del betlist
            del playerstate['for_db']['bill']
	    
            #update total_winlose
            credit_info = playerstate['for_db']['playerinfo']['credit']
            if game_id in credit_info:
                rest_credit = credit_info[game_id]
                rest_credit += total_winlose
                credit_info[game_id] = rest_credit
                playerstate['for_db']['playerinfo']['credit'] = credit_info
                _db.update(playerstate)

def get_info(playerdata):
    return json.loads(playerdata)
