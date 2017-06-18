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
        header.update(msg)
        self._socket.send_json(header)

    def get_uid(self):
        return self._uuid

class player_list(object):

    def __init__(self):
        self._players = list()

    def get_player_num(self):
        return len(self._players)

    def add_player(self, player):
        logging.info("add_player")
        self._players.append(player)

    def remove_player(self, uid):
        logging.info("remove_player")

        player = None
        for p in self._players:
            if p.get_uid() == uid:
                player = p

        if player != None:
            self._players.remove(player)

    def broadcast(self, msg):
        if self.get_player_num() == 0:
            return

        for player in self._players:
            player.send_msg(msg)

    def query_uid(self):

        player_uid = []
        for player in self._players:
            player_uid.append(player.get_uid())
        return  player_uid