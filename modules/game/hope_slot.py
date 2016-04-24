import json

from slot_mgr import *


slot_mgr = game_mgr("slot_mgr")


def handle(json_msg,socket_list):
    print json_msg

    socket = socket_list[0]
    rep = temp_handle(json_msg,socket_list[1])
    socket.send_json(rep)

def temp_handle(json_msg,db):

    #TODO asking gmr in db, ok

    #create by return id or fail repley ( ex, join fail or open fail) ok

    #creat game ok ,leave remove

    if json_msg['cmd'] == "request_join":
       join_room = json_msg['module']
       result = db.get(join_room)

       #create db game data
       if result == None :
           db.create_game(join_room,json_msg['uuid'])
       else:
          print "room open"
          print result
 
       #create game instance
       create_msg = slot_mgr.order("test")
       print create_msg

       rep = header(json_msg)
       rep['state'] = "game_join_ok"

       #TODO gamestart
       rep['init_info'] = "you get init"

       rep['UserPoint'] = 100
       rep['Line'] = 30
       rep['Symbol_Num'] = 8
       odds = dict()
       odds['N0'] = [0 , 0 , 5  , 15 , 50]
       odds['N1'] = [0 , 0 , 10  , 20 , 60]
       odds['N2'] = [0 , 0 , 15  , 40 , 80]
       odds['N3'] = [0 , 0 ,20  , 60 , 100]
       odds['N4'] = [0 , 5 , 25  , 80 , 150]
       odds['N5'] = [0 , 10 ,30   ,100 , 200]
       odds['N6'] = [0 , 15 ,50   ,200 , 200]
       odds['N7'] = [0 , 15 ,100   ,300 ,600]
       odds['W'] = [0 , 20 ,200   ,500 ,800]
       odds['S'] = [0 , 0 ,0 ,0 ,0]
       rep['odds'] = odds

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

