import uuid
import json
import time
from collections import *
from protocol import *
import logging


class PlayerInfo(object):

    def __init__(self):
        logging.info("player init")
        self._real_ip = None

    def connect_success(self,ip):
        self._real_ip = ip
        msg = self.header(MSG_TYPE_LOGIN)
        self.write_message(msg)

    def login_result(self, login_result, playerinfo):
        if login_result:
            self._playerinfo = playerinfo
            LobbyInfo = self.header(MSG_TYPE_LOBBY)
            self.write_message(LobbyInfo)

        else:
            LoginFail = self.header(MSG_TYPE_LOGIN_ERROR)
            self.write_message(loginFail)

    def game_Lobby_info(self, game_type):
        # first customized package
        # self.send_msg(MSG_TYPE_GAME_LOBBY,msg)
        game_lobby_info = self.header(MSG_TYPE_GAME_LOBBY)
        self.write_message(game_lobby_info)

    def into_game(self, room_num):
        self.myGame.into_game(room_num)
        self.myGame.playerlist.add_player(self)

        # put in where?
        inside_game_info = self.header(MSG_TYPE_INTO_GAME)
        inside_game_info['inside_game_info'] = self.myGame.inside_game_info()
        self.write_message(inside_game_info)

    def game_msg(self, data):
        self.myGame.msg_handler(self, data)

    def disconnect(self):
        logging.info("disconnect")
        if self.myGame is not None:
            self.myGame.playerlist.remove_player(self)
            self.myGame.disconnect()

    def get_player_info(self):
        return self._playerinfo

    def get_player_ip(self):
        return self._real_ip
 
    def updata_credit(self, amount):
        self._playerinfo["credit"] += amount

    def send_msg(self, msgtype, msg):
        header = self.header(msgtype)
        header.update(msg)
        self.write_message(header)

    def header(self, msg_type):
        header = OrderedDict()
        header["id"] = str(uuid.uuid4())
        header["timestamp"] = time.time()
        header["message_type"] = msg_type
        return header

    # send message to socket
    def write_message(self, message):
        json_string = json.dumps(message)
        self.socket.write_message(json_string)
