import json
from player import *

from slot_mgr import *


slot_mgr = game_mgr("slot_mgr")


def handle(json_msg,socket_list):
    #print json_msg

    socket = socket_list[0]
    rep = temp_handle(json_msg,socket_list)
    socket.send_json(rep)

def temp_handle(json_msg,socket_list):

    player_socket = socket_list[0]
    db = socket_list[1]
    print "game get cmd %s" % json_msg['cmd']

    if json_msg['cmd'] == "request_join":
       module = json_msg['module']
       room = json_msg['room']
       config = module + "_" + room
       result = db.get(config)

       rep = header(json_msg)

       #create db game data
       if result == None :
           db.create_game(json_msg['uuid'],module,room)

           #create game instance
           player = player_info(json_msg['uuid'],player_socket)
           init_msg = slot_mgr.spawn(module,room,player)
           rep['state'] = "game_join_ok"
           rep['proxy_id'] = json_msg['proxy_id']
           rep['playing_module'] = module
           rep['playing_group'] = config
           db.save(rep)

           rep['Line'] = init_msg['Line']
           rep['Symbol_Num'] = init_msg['Symbol_num']
           rep['odds'] = init_msg['odds']
           rep['game_id'] = init_msg['game_id']

       else:
          print "room open"
          game_info = json.loads(result)
          #not myself 
          if game_info['creater'] != json_msg['uuid'] :
              rep['state'] = "game_join_fail"
              rep['error_code'] = "room open by other"
          else:
              print "self game get init msg"
              #TODO keep seat func ,creat game by db state
              #TODO game_info['module'] && config
              #TODO versu_game join player   
              player = player_info(json_msg['uuid'],player_socket)
              init_msg = slot_mgr.spawn(game_info['module'],game_info['room'],player)
              rep['state'] = "game_join_ok"
              rep['proxy_id'] = json_msg['proxy_id']
              rep['playing_module'] = module
              rep['playing_group'] = config
              db.save(rep)

              rep['Line'] = init_msg['Line']
              rep['Symbol_Num'] = init_msg['Symbol_num']
              rep['odds'] = init_msg['odds']
              rep['game_id'] = init_msg['game_id']
#              rep['room'] = init_msg['']

       
       playerstate = json.loads(db.get(json_msg['uuid']))
       info = playerstate['for_db']
       data =  info['playerinfo']
       rep['UserPoint'] = data['credit']

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

        #close game ,return to lobby
        slot_mgr.del_game(json_msg['game_id'])
        rep = header(json_msg)
        rep['module'] = "lobby"
        rep['cmd'] = "request_gamelist"
        return rep

    #close whole windows but network is still working,so can send message to auth
    if json_msg['cmd'] == "lost_connect":
        slot_mgr.del_game(json_msg['game_id'])
        rep = header(json_msg)
        rep['cmd'] = "self_close"
        rep['state'] = "self_close"
        db.save(rep)
        return rep

    if json_msg['cmd'] == "gamespin":
        totalBet = json_msg['Line'] * json_msg['Bet']
        rep = header(json_msg)
        rep['state'] = "spin_result"
        rep['gameResult'] = fake_react()

        return rep

    if json_msg['cmd'] == "gamefreespin":
#       json_msg['freecount']
        rep = header(json_msg)
        rep['state'] = "spin_result"
        rep['gameResult'] = fake_react()
        return rep


def fake_react():
    fake = dict()
    game_result = dict()
    game_result['state'] = 1
    game_result['grid'] = ["N0","N1","N2","N3","N4","N5","N6","N7","W","S","B","B","N1","N2","N7"]
    game_result['winLine'] =[ "1@3@200" , "8@3@2500" , "21@3@300" ]
    game_result['bonusWin'] = [0,0,0]
    game_result['freeMode'] = False
    game_result['freeCount'] = 0
    game_result['freeTotalCount'] = 0
    game_result['freeTotalPoint'] = 0
    game_result['userPoint'] = 200  #after spin point
    game_result['nowJackPot'] = 10000  #jp
    game_result['winJackPotPoint'] = 0

    return game_result

def normal_handle(json_msg):

    if json_msg['cmd'] == "request_join":
#    if json_msg['cmd'] == "request_open":
#       wait in backi( match algo),ready, open a game to service

       # get info from redis
       # 
       rep = header(json_msg)
       rep['state'] = "game_join_ok"

       #TODO gamestart
       rep['init_info'] = "you get init"
       return rep


def header(json_msg):

    rep = dict()
    rep['uuid'] = json_msg['uuid']
    rep['key'] = json_msg['uuid']
    rep['for_db'] = None
    return rep

