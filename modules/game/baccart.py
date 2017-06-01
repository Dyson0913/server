import json
from player import *

from baccart_mgr import *

mgr = game_mgr("mgr")


def handle(json_msg,socket_list):
    #print json_msg

    socket = socket_list[0]
    rep = temp_handle(json_msg,socket_list)
    socket.send_json(rep)

def temp_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    db = socket_list[1]
    print "game get cmd %s" % json_msg['cmd']
    print json_msg

    if json_msg['cmd'] == "request_join":
       module = json_msg['module']
       room = str(json_msg['room'])
       serial_id = module + "_" + room
       result = db.get(serial_id)

       rep = header(json_msg)

       #create db game data
       if result == None :
           db.create_game(json_msg['uuid'],module,room)

           #create game instance
           player = player_info(json_msg['uuid'],player_socket)
           init_msg = mgr.spawn(serial_id,player)
           rep['state'] = "game_join_ok"
           rep['proxy_id'] = json_msg['proxy_id']
           rep['playing_module'] = module
           rep['playing_group'] = serial_id
           db.save(rep)

           rep.update(init_msg)
       else:
           #find game and join
           player = player_info(json_msg['uuid'],player_socket)
           init_msg = mgr.join_game(serial_id,player)
           rep['state'] = "game_join_ok"
           rep['proxy_id'] = json_msg['proxy_id']
           rep['playing_module'] = module
           rep['playing_group'] = serial_id
           db.save(rep)

           rep.update(init_msg)

       return rep

    #self chose leaving game
    if json_msg['cmd'] == "leave_game":
        
        #TODO multi serve handle         
        #playerstate = json.loads(db.get(json_msg['uuid']))
        #uniq_id = playerstate['proxy_id']
        #server_ip = socket_list[2]
        #if uniq_id == server_ip:
        #    print "self server!!! close"
        #    return None
        #else:
        #    print "not my server pass"
            
        #    to_other_proxy = header(json_msg)
        #    to_other_proxy['trans'] = uniq_id
#            to_other_proxy['module'] = "lobby"
#            to_other_proxy['cmd'] = "request_gamelist"
        #    return to_other_proxy
        module = json_msg['module']
        room = str(json_msg['room'])
        serial_id = module + "_" + room
        game_info = db.get(serial_id)

        #can't close if not create
        json_game_info = get_info(game_info)
        if json_game_info['creater'] == json_msg['uuid']:
            mgr.del_game(json_msg['game_id'])

        #return point
        rep = header(json_msg)
        rep['module'] = "credit"
        rep['cmd'] = "return_point_from_game"
        rep['game_serial'] = serial_id

        # rep = header(json_msg)
        # rep['module'] = "lobby"
        # rep['cmd'] = "request_gamelist"
        return rep

    #close whole windows but network is still working,so can send message to auth
    if json_msg['cmd'] == "lost_connect":
        mgr.del_game(json_msg['game_id'])
        rep = header(json_msg)
        rep['cmd'] = "self_close"
        rep['state'] = "self_close"
        db.save(rep)
        return rep

    if json_msg['cmd'] == "bet":
#        totalBet = json_msg['Line'] * json_msg['Bet']
#        rep = header(json_msg)
#        rep['state'] = "spin_result"
        # get game in db & get spin result msg
#        rep['gameResult'] = fake_react()
        pass
#        return rep

    if json_msg['cmd'] == "cancel_bet":
#       json_msg['freecount']
#        rep = header(json_msg)
#        rep['state'] = "spin_result"
#        rep['gameResult'] = fake_react()
#        return rep
        pass

def header(json_msg):

    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

def get_info(playerdata):
    return json.loads(playerdata)

