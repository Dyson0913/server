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
        if self._socket == None :
            return

        header = self.header()
        header.update(msg)
        self._socket.send_json(header)

    def get_uid(self):
        return self._uuid

class player_list(object):

    def __init__(self):
        self._players = list()
        self._lost_Connect_player = list()

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
                #if game not settle leving,recode for settle
                self._lost_Connect_player.append(uid)

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
            uid  = player.get_uid()

            # leaving user come back before settle,remove uid
            if uid in self._lost_Connect_player:
                self._lost_Connect_player.remove(uid)

            player_uid.append(uid)

        #leaving user not come back,need to settle
        for id in self._lost_Connect_player:
            player_uid.append(id)

        del self._lost_Connect_player[:]

        return  player_uid