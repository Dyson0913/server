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

    def broadcast(self, msg):
        if self.get_player_num() == 0:
            return

        for player in self._players:
            player.send_msg(msg)