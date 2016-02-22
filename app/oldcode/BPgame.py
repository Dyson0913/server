from game_protocol import *
from core_protocol import *
from collections import *
from state import *
from poker import *
import baccarat_settle
import bigwin_settle
import perfectangel_settle
import datetime
#from BPgame_paytable import *
import BPgame_paytable
import logging

class BPgame(object):

    def __init__(self,gametype):
        self._banker = []
        self._player = []
        self._river = []
        self._state = 0
        self._remain_time = 0
        self._winstate = 0
        self._gametype = gametype;

    def reset(self):
        del self._banker[:]
        del self._player[:]
        del self._river[:]

    def zmqmsg(self,msg):
        if msg['message_type'] == MSG_TYPE_SYC_TIME:
            self._remain_time = msg['remain_time']
        elif msg['message_type'] == MSG_TYPE_STATE_INFO:
            #BPgame decide self
            #self._gametype = msg['game_type']
            self._remain_time = msg['remain_time']
            self._state = msg['games_state']
            if self._state == STATE_NEW_ROUND:
                self.reset()
            elif self._state == STATE_END_BET:
                #update bet amount
                self.playerlist.dealer.update_credit()
            self.send_game_info()
        elif msg['message_type'] == MSG_TYPE_GAME_OPEN_INFO:
            if msg['type'] == MSG_TYPE_BANKER_CARD:
                self._banker += msg['card'];
                logging.info("deal_banker_card %s" % msg['card'])
                self.send_poker(msg['type'], self._banker)
            elif msg['type'] == MSG_TYPE_PLAYER_CARD:
                self._player += msg['card'];
                logging.info("deal_player_card %s" % msg['card'])
                self.send_poker(msg['type'], self._player)
            elif msg['type'] == MSG_TYPE_RIVER_CARD:
                self._river += msg['card'];
                logging.info("deal_player_card %s" % msg['card'])
                self.send_poker(msg['type'], self._river)
        elif msg['message_type'] == MSG_TYPE_ROUND_INFO:

            self._winstate = msg['winstate']
            msg = dict()
            msg["Action"] = "putGameResult"
            msg["GameType"] = self._gametype
            msg["GameDate"] = self.get_time()
            msg["GameTable"] = 2
            msg["GameCode"] = "2-20"
            if self._gametype == 2:
                msg["GameResult"] = PokerPoint.get_db_mapping(self._banker)+"#"+PokerPoint.get_db_mapping(self._player)+"#"+PokerPoint.get_db_mapping(self._river)
            else:
                msg["GameResult"] = PokerPoint.get_db_mapping(self._banker)+"#"+PokerPoint.get_db_mapping(self._player)
            msg["GameStatus"] = 1

            self.recoder.write_back(msg)
            # wait for ResultID

    def get_ResultID(self,ResultID):

        msg = dict()
        msg["Action"] = "putOrderInfo"
        msg["GameType"] = self._gametype
        msg["MachineCode"] = 0
        msg["ResultID"] = ResultID
        msg["OrderDate"] = self.get_time()

        self.playerlist.dealer.settle(self._winstate)
        self.playerlist.write_back_info(self._winstate,self.recoder,msg)

        msg = self.get_end_round_info(self._winstate)
        self.playerlist.broadcast_with_self_info(MSG_TYPE_ROUND_INFO, msg)

        self.playerlist.dealer.clean_bet()

    def get_time(self):
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def get_game_info(self):
        msg = dict()
        msg["game_type"] = self._gametype
        msg["games_state"] = self._state
        return msg

    def send_game_info(self):
        msg = self.get_game_info()
        msg["remain_time"] = self._remain_time
        self.playerlist.broadcast(MSG_TYPE_STATE_INFO, msg)
   
    def send_poker(self, card_type, card):
        msg = self.get_poker(card_type, card)
        self.playerlist.broadcast(MSG_TYPE_GAME_OPEN_INFO, msg)

    def get_poker(self, card_type, poker):
        msg = self.get_game_info()
        card = dict()
        card["card_type"] = card_type
        card["card_list"] = poker
        msg["card_info"] = card
        return msg

    def get_end_round_info(self, round_result):
        msg = self.get_game_info()
        msg["remain_time"] = self._remain_time
        msg["win_type"] = round_result
        return msg

    def into_game(self, room_num):
        pass #logging.info("enter bigwin")

    def inside_game_info(self):
        msg = self.get_game_info()
        msg["remain_time"] = self._remain_time
        msg["player_info"] = self.playerlist.get_enter_player()
        msg["split_symbol"] = self.paytable.split_symbol()
        msg["bet_zone"] = self.paytable.bet_zone()
        card = dict()
        card["player_card_list"] = self._player
        card["banker_card_list"] = self._banker
        if self._gametype == 2:
            card["river_card_list"] = self._river
        msg["game_info"] = card
        return msg

    def msg_handler(self, player, data):
        if data['message_type'] == MSG_TYPE_BET:
            result = self.playerlist.dealer.new_bet(
                player,
                data['amount'],
                data['bet_type'])
            msg = self.get_bet_info(result, data['serial_no'])
            player.send_msg(MSG_TYPE_BET_INFO, msg)

    def get_bet_info(self, result, serial_no):
        msg = OrderedDict()
        msg["serial_no"] = serial_no
        msg["game_type"] = self._gametype
        msg["result"] = result
        return msg

    def disconnect(self):
        pass #logging.info("bigwin disconnect")
