
from tornado import gen, tcpclient
from tornado.ioloop import IOLoop, PeriodicCallback
#from state import *
from ball5enc import *
from poker import *
from collections import *
import sys
import zmq
import json
from core_protocol import *
#from skydef import *
from game_protocol import *
from pylog import *
from corewitharm import *
from corenormal import *

Key = [ 0x03, 0x2C, 0x23, 0x2A, 0xCB, 0x85, 0x76, 0xE2, 0x85, 0x93, 0x4B, 0x80, 0xE1, 0x5C, 0x48, 0xE1 ]

class CoreServer(object):

    loop = None
    tcp_reset = None
    tcp_main = None
    sock_reset = None
    sock_main = None
    sock_pub = None


    def __init__(self):
        self.witharm = True
        self._banker = []
        self._player = []
        self._river = []
        self._poker = Poker()
        self.pinpon = 0

    def start(self):
        print "coreserver start"
        if self.witharm == True:
            self.tcp_reset = tcpclient.TCPClient()
            self.tcp_main = tcpclient.TCPClient()
            self._init_state = ArmInitState(self)
            self._new_round_state = ArmNewRoundState(self,10)
            self._end_bet_state = ArmEndBetState(self)
            self._end_round_state = ArmEndRoundState(self)
            self.recv_callback = PeriodicCallback(self.recv_arm_msg, 100)
        else:
            self._init_state = NormalInitState(self)
            self._new_round_state = NormalNewRoundState(self,10)
            self._end_bet_state = NormalEndBetState(self)
            self._end_round_state = NormalEndRoundState(self)

        self.loop = IOLoop.instance()
        context = zmq.Context()
        self.sock_pub = context.socket(zmq.PUB)
        if self.gametype == 1:
            self.sock_pub.bind("tcp://*:5556")
        elif self.gametype == 2:
            self.sock_pub.bind("tcp://*:5557")
        elif self.gametype == 3:
            self.sock_pub.bind("tcp://*:5558")
        
        self.time_callback = PeriodicCallback(self.update_time, 1000)
        

        self.set_state(self._init_state)

        self.time_callback.start()
        try:
            self.loop.start()
        except KeyboardInterrupt:
            pass


    @gen.coroutine
    def arm_reset(self):
        logging.debug("arm_reset")
        try:
            self.sock_reset = yield self.tcp_reset.connect('220.132.215.90', 5031)
            logging.info("Reset Port Connected !!!")
        except Exception as e:
            logging.info("Reset Port Caught Error: %s" % e)

    @gen.coroutine
    def arm_connect(self):
        try:
            self.sock_main = yield self.tcp_main.connect('220.132.215.90', 5032)
            logging.info( "Arm Port Connected !!!" )
            self.recv_callback.start()    
        except Exception as e:
            logging.info( "Arm Port Caught Error: %s" % e )

    def make_msg(self, cmd, *args):
        msg = ""
        msg += str(cmd)
        for arg in args:
            msg += ","
            msg += str(arg)

        return msg

    def send_arm_msg(self, cmd, *args):
        msg = self.make_msg(cmd, *args)
        enc_msg = encrypt_command(msg, Key)
        logging.info( 'sending raw: %s enc: "%s"' % (msg, enc_msg) )
        self.sock_main.write(enc_msg)

    def send_deal_card_msg(self):
        delay_secs = 0
        if self.pinpon:
            self.send_arm_msg(SKY_SERVER_CMD_DEAL_CARD, SKY_BRANDBOOT_2, delay_secs)
            self.pipon = 0
        else:
            self.send_arm_msg(SKY_SERVER_CMD_DEAL_CARD, SKY_BRANDBOOT_1, delay_secs)
            self.pipon = 1

    def update_recv_arm_msg(self, command):
        event = dict()
        event['type'] = EVT_RECV_ARM_MSG
        event['data'] = command
        logging.info( "update_recv_arm_msg %s" % command )
        self._state.update_event(event)

    def on_body(self, data):
        dec_command = decrypt_command(data, Key)
        self.update_recv_arm_msg(dec_command)
        
        #return dec_command

    def on_headers(self,data):
        data_len = int(data[:-1])
        self.sock_main.read_bytes(data_len, self.on_body) 
        #return dec_command

    def recv_arm_msg(self):
        if self.sock_main == None:
            return
        if self.sock_main.reading() != True:
            self.sock_main.read_until(";", self.on_headers)
    
    def set_state(self, new_state):
        self._state = new_state
        self._state.enter_state()

    def reset(self):
        del self._banker[:]
        del self._player[:]
        del self._river[:]
        #self.send_shuffle_msg()
        self._poker.shuffle()

    def newround(self):
        self.reset()
        self.send_game_info()

    def endbet(self):
        logging.info( "endbet" )
        self.send_game_info()

    def get_player_crd_num(self):
        logging.info( "player card num: %d" % len(self._player) )
        return len(self._player)

    def get_banker_card_num(self):
        logging.info( "banker card num: %d" % len(self._banker) )
        return len(self._banker)
    
    def deal_player_card(self, card):
        msg = dict()
        msg['type'] = MSG_TYPE_PLAYER_CARD
        msg['card'] = card 
        msg['message_type'] = MSG_TYPE_GAME_OPEN_INFO
        self._player += card
        logging.info( "deal_player_card %s num %d" % (card, len(self._player)) )
        logging.info( self._player )
        self.publish(msg)

    def deal_banker_card(self, card):
        msg = dict()
        msg['type'] = MSG_TYPE_BANKER_CARD
        msg['card'] = card
        msg['message_type'] = MSG_TYPE_GAME_OPEN_INFO
        self._banker += card
        logging.info( "deal_banker_card %s num %d" % (card, len(self._banker)) )
        logging.info( self._banker )
        self.publish(msg)

    def deal_river_card(self, card):
        msg = dict()
        msg['type'] = MSG_TYPE_RIVER_CARD
        msg['card'] = card
        msg['message_type'] = MSG_TYPE_GAME_OPEN_INFO
        self._river += card
        logging.info( "deal_river_card %s num %d" % (card, len(self._river)) )
        logging.info( self._river )
        self.publish(msg)

    def deal_player_card_from_poker(self):
        card = self._poker.deal_cards(1)
        self.deal_player_card(card)

    def deal_banker_card_from_poker(self):
        card = self._poker.deal_cards(1)
        self.deal_banker_card(card)

    def deal_river_card_from_poker(self):
        card = self._poker.deal_cards(1)
        self.deal_river_card(card)

    def update_time(self):
        self._state.update_time()
        self.syc_remain_time()

    def publish(self, message):
        logging.info( message )
        #json_string = json.dumps(message)
        #logging.info( type(json_string) )
        #self.sock_pub.send_string(json_string)
        self.sock_pub.send_json(message)

    def get_game_info(self):
        msg = dict()
        msg["game_type"] = MSG_TYPE_RUNGAME
        state = STATE_INITIAL
        if self._state == self._new_round_state:
            state = STATE_NEW_ROUND
        elif self._state == self._end_bet_state:
            state = STATE_END_BET
        elif self._state == self._open_state:
            state = STATE_START_ROUND
        elif self._state == self._end_round_state:
            state = STATE_END_ROUND
        msg["games_state"] = state
        return msg
   
    def send_game_info(self):
        msg = self.get_game_info()
        msg["remain_time"] = self._state.get_remain_time()
        msg["message_type"] = MSG_TYPE_STATE_INFO
        self.publish(msg);

    def syc_remain_time(self):
        msg = dict() 
        msg["remain_time"] = self._state.get_remain_time()
        msg["message_type"] = MSG_TYPE_SYC_TIME
        self.publish(msg);

    def check_result(self):
        pass


