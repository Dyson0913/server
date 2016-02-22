from state import *
from skydef import *
from coreserver import *
from poker import *
from baccaratarm import *
from baccaratnormal import *
from di import *
from optparse import OptionParser
import pylog
from ba_paytable import *
import ba_paytable


class Baccarat(CoreServer):

    def start(self):
        if self.witharm == True:
            self._open_state = baccaratArmOpenState(self)
        else:
            self._open_state = baccaratOpenState(self)

        super(Baccarat, self).start()

    def player_top_card_rule(self):
        return PokerPoint.check_baccarat_top_card_rule(self._player) or PokerPoint.check_baccarat_top_card_rule(self._banker) 

    def player_extra_card(self):
        if self.get_banker_card_num() == 2:
            return PokerPoint.check_baccarat_player_extra_card_rule(
                self._player)
        else:
            return False

    def banker_extra_card(self):
        return PokerPoint.check_baccarat_banker_extra_card_rule(
            self._player,
            self._banker)

    def check_result(self):
        logging.info("balance")
        winstate = ""
        playerpoint = PokerPoint.get_baccarat_point(self._player)
        bankerpoint = PokerPoint.get_baccarat_point(self._banker)
        if playerpoint > bankerpoint:
            logging.info("player win")
            winstate += ba_paytable.combine_winstate(Baccarat_player,ba_odds_1)
        elif playerpoint < bankerpoint:
            logging.info("banker win")
            winstate += ba_paytable.combine_winstate(Baccarat_banker,ba_odds_095)
        else:
            logging.info("tie")
            winstate += ba_paytable.combine_winstate(Baccarat_tie,ba_odds_8)
            # pair
            # playerpoint = PokerPoint.get_baccarat_point(self.playerpoker[2:])
            # bankerpoint = PokerPoint.get_baccarat_point(self.bankerpoker[2:])
            # if playerpoint > bankerpoint:
            #     winstate = Baccarat.wintype_pair

        msg = dict()
        msg['winstate'] = winstate
        msg['paytable'] = ba_paytable.paytable(winstate)
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
        core = inject(Baccarat, witharm = True, gametype = options.game)
    else:
        print "false"
        core = inject(Baccarat, witharm = False, gametype = options.game)

    core.start()


if __name__ == '__main__':
    
    main()
 

