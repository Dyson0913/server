import datetime

#######################################################
# the class which mantain game state
#
#   ###########             ###########
#   #         #   timeout   #         #
#   #New Round#------------># End Bet #         
#   #         #             #         # 
#   ###########             ###########
#       /|\                      |
#        |                       | timeout
#        | timeout               |
#        |                      \|/
#   ###########             ###########    
#   #   End   #             #  Start  #<-----|
#   #         #<------------#  Open   #      | open next ball
#   #  Round  #             #  Ball   #      |
#   ###########             ###########------|
#
######################################################
class BankerPlayerGameControl(object):

    _INITIAL = 0
    _NEW_ROUND = 1
    _END_BET = 2
    _START_ROUND = 3
    _END_ROUND = 4 
    _INITIAL_TIMEUP = datetime.timedelta(seconds=6)
    
    state_map = {}  
    
    def __init__(self,new_round_timeup=30, end_bet_timeup=2, open_timeup=2, end_round_timeup=4):
        self._state = BankerPlayerGameControl._INITIAL 
        self._state_time = datetime.datetime.now()

        self.state_map[BankerPlayerGameControl._INITIAL] = BankerPlayerGameControl._INITIAL_TIMEUP
        self.state_map[BankerPlayerGameControl._NEW_ROUND] = self.set_time(new_round_timeup)
        self.state_map[BankerPlayerGameControl._END_BET] =  self.set_time(end_bet_timeup)
        self.state_map[BankerPlayerGameControl._START_ROUND] = self.set_time(open_timeup)
        self.state_map[BankerPlayerGameControl._END_ROUND] = self.set_time(end_round_timeup)
    
    def set_time(self,sec):
        return datetime.timedelta(seconds = sec)   
 
    def is_state_timeup(self):
        timediff = datetime.datetime.now() - self._state_time
        if timediff > self.state_map[self._state]:
            return True

        return False

    def goto_new_round(self):
        self._state = BankerPlayerGameControl._NEW_ROUND
        self._state_time = datetime.datetime.now()

    def goto_end_bet(self):
        self._state = BankerPlayerGameControl._END_BET
        self._state_time = datetime.datetime.now()

    def in_start_round(self):
        self._state_time = datetime.datetime.now()
     
    def check_game_state(self):

        if self.is_state_timeup():
            if self._state == BankerPlayerGameControl._INITIAL:
                print "goto_new_round"
                self.goto_new_round()
                
            elif self._state == BankerPlayerGameControl._NEW_ROUND:
                print "goto_end_bet"
                self.goto_end_bet()
                
            elif (self._state == BankerPlayerGameControl._END_BET) or (self._state == BankerPlayerGameControl._START_ROUND) :
                if self._state == BankerPlayerGameControl._END_BET:
                    self._state = BankerPlayerGameControl._START_ROUND
                print "in_start_round"
                self.in_start_round()
                
            elif (self._state == BankerPlayerGameControl._END_ROUND):
                print "end_round goto_new_round"
                self.goto_new_round()

       

    def get_remain_time(self):
        timediff = datetime.datetime.now() - self._state_time

        diff = self.state_map[self._state] - timediff
        return diff.seconds

