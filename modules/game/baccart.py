import json

from baccart_mgr import *

mgr = game_mgr("mgr")

_db = None

def handle(json_msg,socket_list):
    #print json_msg

    socket = socket_list[0]
    rep = temp_handle(json_msg,socket_list)
    socket.send_json(rep)

def temp_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    global _db
    _db = socket_list[1]
    print "game get cmd %s" % json_msg['cmd']

    if json_msg['cmd'] == "request_join":
       module = json_msg['module']
       room = str(json_msg['room'])
       serial_id = module + "_" + room
       uid = json_msg['uuid']
       result = _db.get(serial_id)

       rep = header(json_msg)

       init_msg = None
       #create _db game data
       if result == None :
           #first user creat,never close
           _db.create_game("**",module,room)
           #create game instance
           init_msg = mgr.spawn(serial_id,uid,player_socket)
       else:
           #find game and join
           init_msg = mgr.join_game(serial_id,uid,player_socket)

       rep['state'] = "game_join_ok"
       rep['proxy_id'] = json_msg['proxy_id']
       rep['playing_module'] = module
       rep['playing_group'] = serial_id
       _db.save(rep)

       rep.update(init_msg)

       return rep

    #self chose leaving game
    if json_msg['cmd'] == "leave_game":
        uid = json_msg['uuid']
        game_id = json_msg['game_id']

        #TODO multi serve handle         
        #playerstate = json.loads(_db.get(json_msg['uuid']))
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

        game_info = _db.get(game_id)

        #remove if create by self
        close_game(game_info,game_id,uid)

        #return point
        return return_point(json_msg,"return_point_from_game")

    #close whole windows but network is still working,so can send message to auth
    if json_msg['cmd'] == "lost_connect":
        uid = json_msg['uuid']
        game_id = json_msg['game_id']

        game_info = _db.get(game_id)
        #lost_connect ,diff handle by game
        close_game(game_info,game_id,uid)

        rep = header(json_msg)
        rep['state'] = "self_close"
        _db.save(rep)

        # return point
        return return_point(json_msg,"just_return_point")

def header(json_msg):
    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

def get_info(playerdata):
    return json.loads(playerdata)

def close_game(game_info,game_id,uid):
    global _db

    json_game_info = get_info(game_info)
    if json_game_info['creater'] == uid:
        mgr.del_game(game_id)
        _db.clean(game_id)
    else:
        mgr.remove_player(game_id,uid)

def return_point(json_msg,cmd):
    rep = header(json_msg)
    rep['module'] = "credit"
    rep['cmd'] = cmd
    rep['game_serial'] = json_msg['game_id']
    return rep
