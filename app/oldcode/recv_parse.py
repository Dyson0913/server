from protocol import *
from di import *

def recv_data(data, player, gamelist):
    if data['message_type'] == MSG_TYPE_LOGIN:
        login_info = data["login_info"]
        # login module process
        playerinfo = demologin(login_info)

        player.login_result(True, playerinfo)

    elif data['message_type'] == MSG_TYPE_SELECT_GAME:
        game_type = data["game_type"]

        # dynamic load game control
        inject(player, myGame=gamelist[0])
        player.game_Lobby_info(game_type)

    elif data['message_type'] == MSG_TYPE_INTO_GAME:
        room_num = data["game_room"]
        player.into_game(room_num)

    elif data['message_type'] > MSG_TYPE_INTO_GAME:
        # pass to game ,each game handle their own package
        player.game_msg(data)

def demologin(info):
    if info != None:
        login_info = info['data']
        userid = login_info["UserID"]
        nickname = login_info["UserAccount"]
        credit = float(login_info["UserGold"])
    else: 
        userid = "1"
        nickname = "fakename"
        credit = 50000
    return {'userid': userid, 'nickname': nickname, 'credit': credit}

