import sys

sys.path.append('../')

from fsm import *
import pylog

class hope_three(object):

      
    def __init__(self,name,symbol_num,rollerNum,line):
        self._win = ""
        self._name = name
        self._rollerNum = rollerNum
        self._line = line
        self._symbol_num = symbol_num
        self._info_to_client = None 
        odds = dict()
        odds['N0'] = [0,0,2,20,200]
        odds['N1'] = [0,0,3,30,300]
        odds['N2'] = [0,0,5,50,500]
        odds['N3'] = [0,0,8,80,800]
        odds['N4'] = [0,0,10,100,1000]
        odds['N5'] = [0,0,15,150,1500]
        odds['N6'] = [0,0,30,300,3000]
        odds['N7'] = [0,0,50,500,5000]
        odds['W'] = [0,0,50,500,5000]
        odds['S'] = [0, 0 ,0 ,0 ,0]
        self._odd = odds


    def flush_state(self,state):
        msg = dict()
        msg['state'] = state
        self._info_to_client = msg

    def test_script(self,script_name,args):
        self._poker.test_script(args)

    def init_msg(self):
        init = dict()
        init['Line'] = self._line
        init['Symbol_num'] = self._symbol_num
        init['odds'] = self._odd

        logging.info( "init msg " + str(init))
        return init

    def msg(self):
        logging.info( "client msg " + str(self._info_to_client))
        return self._info_to_client

    def reset(self):
        del self._banker[:]
        del self._player[:]
        self._poker.shuffle()

    def settle(self):
        logging.info( "settle" )


class init(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "NG"

    def update(self):
        print "ini update"

class NG(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "NG"

    def update(self):
        print "NG update"
            #self.next_state = "FG"
            #self.next_state = "JP"

class FG(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "NG"

    def execute(self):
        pass

class JP(State):

    def __init__(self,stay_period):
        self.period = stay_period
        self.name = self.__class__.__name__
        self.next_state = "NG"

    def execute(self):
        pass 

def main():
    
    mygame = hope_three("main_hopethree",8,5,30)

    myfms = fms()
    setattr(myfms,'app',mygame)
    myfms.add(init(-1))
    myfms.add(NG(-1))
    myfms.add(FG(-1))
    myfms.add(JP(-1))

    myfms.start("init")

if __name__ == "__main__":
    main()

 
