from bigwinarm import *
from bigwinnormal import *
from state import *
from skydef import *
from coreserver import *
from poker import *
from optparse import OptionParser
from di import *
from big_paytable import *
import big_paytable


class BigWin(CoreServer):


    def start(self):
        if self.witharm == True:
            self._open_state = BigWinArmOpenState(self)
        else:
            self._open_state = BigWinOpenState(self)
        
        super(BigWin, self).start()

    def check_result(self): 
        total_cards = self._banker + self._player + self._river
        logging.info("total card %s" % total_cards)
        value = PokerPoint.check_big_win_show_hand(total_cards)
        winstate = ""
        if value == PokerPoint.POKER_ROYAL_FLUSH:
            winstate += big_paytable.combine_winstate(bigwin_banker,big_odd_1000)
        elif value == PokerPoint.POKER_STRAIGHT_FLUSH:
            winstate += big_paytable.combine_winstate(bigwin_banker,big_odd_100)
        elif value == PokerPoint.POKER_FOUR_OF_A_KIND:
            winstate += big_paytable.combine_winstate(bigwin_banker,big_odd_40)
        elif value == PokerPoint.POKER_FULL_HOUSE:
            winstate += big_paytable.combine_winstate(bigwin_banker,big_odd_10)
        elif value == PokerPoint.POKER_FLUSH:
            winstate += big_paytable.combine_winstate(bigwin_banker,big_odd_6)
        elif value == PokerPoint.POKER_STRAIGHT:
            winstate += big_paytable.combine_winstate(bigwin_banker,big_odd_4)
        else:
            banker_point = PokerPoint.get_baccarat_point(self._banker)
            player_point = PokerPoint.get_baccarat_point(self._player)
            if banker_point > player_point:
                logging.info("banker win")
                winstate += big_paytable.combine_winstate(bigwin_banker,big_odds_1)
            elif player_point > banker_point:
                logging.info("player win")
                winstate += big_paytable.combine_winstate(bigwin_player,big_odds_1)
	    else:
                logging.info("tie")
                winstate += big_paytable.combine_winstate(bigwin_banker,big_odds_0)

        msg = dict()
        msg['winstate'] = winstate
        msg['paytable'] = big_paytable.paytable(winstate)
        msg['message_type'] = MSG_TYPE_ROUND_INFO
        self.publish(msg)


def main():


    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage) 
   
    parser.add_option("-a", "--arm", action="store_true", default=False)
    parser.add_option("-g", "--game" ,default=1,type=int)
    (options, args) = parser.parse_args()


    if options.arm == True:
        print "true"
        core = inject(BigWin, witharm = True,gametype = options.game)
    else:
        print "false"
        core = inject(BigWin, witharm = False,gametype = options.game)

    core.start()

if __name__ == '__main__':
    
    main()
 

