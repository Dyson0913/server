import logging


class player_info(object):

    def __init__(self,uuid,socket):
        self._uuid = uuid
        self._socket = socket

    def header(self):
        rep = dict()
        rep['uuid'] = self._uuid
        return rep

    def send_msg(self,msg):
        header = self.header()
        print "header"
        print header
        header.update(msg)
        print header
        self._socket.send_json(header)

class player_list(object):

    def __init__(self):
        self._players = list()

    def get_player_num(self):
        return len(self._players)

    def add_player(self, player):
        logging.info("add_player")
        self._players.append(player)

    def remove_player(self, player):
        logging.info("remove_player")
        self._players.remove(player)
        #TODO leave before settle

    def broadcast(self, msg):
        if self.get_player_num() == 0:
            return

        for player in self._players:
            player.send_msg(msg)

    def broadcast_with_self_info(self, msgtype, msg):
        if self.get_player_num() == 0:
            return

        for player in self._players:
            msg["player_info"] = player.get_player_info()
            msg["bet_amount"] = self.dealer.get_player_bet(player)
            msg["settle_amount"] = self.dealer.get_player_settle(
                player,
                msg["win_type"]
                )
            player.send_msg(msgtype, msg)


    def write_back_info(self, wintype,recoder, msg):
        if self.get_player_num() == 0:
            return

        for player in self._players:
            betinfo = self.dealer.get_db_settle(player)
            if betinfo != None:
                playerinfo = player.get_player_info()
                msg["UserID"] = playerinfo['userid']
                msg["UserGold"] = playerinfo['credit']
                msg["BetList"] = betinfo
                msg["OrderIP"] = player.get_player_ip()
                msg["OrderStatus"] = 1
                recoder.write_back(msg)

