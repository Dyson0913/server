import json

from slot_mgr import *


slot_mgr = game_mgr("slot_mgr")


def handle(json_msg,socket_list):
    print json_msg

    socket = socket_list[0]
    rep = temp_handle(json_msg,socket_list[1])
    socket.send_json(rep)

def temp_handle(json_msg,db):

    #creat game ok ,leave remove

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
           init_msg = slot_mgr.spawn(module,room)
           #create game instance
           rep['state'] = "game_join_ok"
           rep['Line'] = init_msg['Line']
           rep['Symbol_Num'] = init_msg['Symbol_num']
           rep['odds'] = init_msg['odds']

       else:
          print "room open"
          game_info = json.loads(result)
          #not myself 
          if game_info['creater'] != json_msg['uuid'] :
              rep['state'] = "game_join_fail"
          else:
              print "self game get init msg"
              #TODO keep seat func ,creat game by db state
              # game_info['module'] && config
                 
              init_msg = slot_mgr.spawn(game_info['module'],game_info['room'])

       
       playerstate = json.loads(db.get(json_msg['uuid']))
       info = playerstate['for_db']
       data =  info['playerinfo']
       rep['UserPoint'] = data['credit']

       return rep

    if json_msg['cmd'] == "gamespin":
#       json_msg['Line']
#       json_msg['Bet']
        rep = header(json_msg)
        rep['state'] = "spin_result"
        rep['GameResult'] = fake_react()

        return rep

    if json_msg['cmd'] == "gamefreespin":
#       json_msg['freecount']
        rep = header(json_msg)
        rep['state'] = "spin_result"
        rep['GameResult'] = fake_react()
        return rep


def fake_react():
    fake = dict()
    game_result = dict()
    game_result['state'] = 1
    game_result['iGrid'] = ["W","S","W","S","W","S","W","S","W","S","W","S","W","S","W"]
    game_result['WinLine'] =[ "1@3@200" , "8@3@2500" , "21@3@300" ]
    game_result['BonusWin'] =[]
    game_result['FreeMode'] = False
    game_result['FreeCount'] = 0
    game_result['FreeTotalCount'] = 0
    game_result['FreeTotalPoint'] = 0
    game_result['UsePoint'] = 200  #after spin point
    game_result['NowJackPot'] = 10000  #jp
    game_result['WinJackPotPoint'] = 0

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

