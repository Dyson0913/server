from state import *
from skydef import *
from poker import *
from coreserver import *
from angelarm import *
from angelnormal import *
from di import *
from optparse import OptionParser
from angel_paytable import *
import angel_paytable


class PerfectAngel(CoreServer):

    def start(self):
    
        if self.witharm == True:
            print "witharm"
            self._open_state = PerfectAngelArmOpenState(self)
        else:
            print "withoutarm"
            self._open_state = PerfectAngelOpenState(self)

        super(PerfectAngel, self).start()



    def check_five_wawa(self):

        banker_five_wawa = PokerPoint.check_newnew_five_wawa(self._banker)
        player_five_wawa = PokerPoint.check_newnew_five_wawa(self._player)
        winstate = ""

        if banker_five_wawa == 0 and player_five_wawa == 0:
            return winstate
       
        if banker_five_wawa > player_five_wawa:
            logging.info("banker_five_wawa win")
            winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_40)
        if player_five_wawa > banker_five_wawa:
            logging.info("player_five_wawa win")
            winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_40)
            return winstate

        if banker_five_wawa == player_five_wawa:
            banker_point = PokerPoint.get_cards_max_order(self._banker)
            player_point = PokerPoint.get_cards_max_order(self._player)
            if banker_point > player_point:
                logging.info("banker_five_wawa win")
                winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_40)
            else:
                logging.info("player_five_wawa win")
                winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_40)

        return winstate

    def check_four_of_a_kind(self):
        
        banker_four_of_a_kind = PokerPoint.check_newnew_four_of_a_kind(self._banker)
        player_four_of_a_kind = PokerPoint.check_newnew_four_of_a_kind(self._player)
        winstate = ""

        if banker_four_of_a_kind ==0 and player_four_of_a_kind==0:
            return winstate

        if banker_four_of_a_kind > player_four_of_a_kind:
            logging.info("banker_four_of_a_kind win")
            winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_40)
        elif player_four_of_a_kind < banker_four_of_a_kind:
            logging.info("player_four_of_a_kind win")
            winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_40)
        else:
            logging.inf("strange condition here")
            winstate = 0

        return winstate

    def check_newnew_point(self):
        banker_point = PokerPoint.get_newnew_point(self._banker)
        player_point = PokerPoint.get_newnew_point(self._player)

        logging.info("banker {0}".format(self._banker))
        logging.info("player {0}".format(self._player))

        logging.info("banker_point={0}, player_point={1}".format(banker_point, player_point))
        
        winstate = ""
        if banker_point == 0 and player_point==0:
            winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_0)
            winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_0)
            logging.info(winstate)
            return winstate

        if banker_point > player_point:
            if banker_point == 2:
                winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_3)
            elif banker_point == 1:
                winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_2)
            else:
                winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_1)

        elif player_point > banker_point:
            if player_point == 2:
                winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_3)
            elif player_point == 1:
                winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_2)
            else:
                winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_1)
        else:
            #same point and we will compare the card detail
            banker_max_order = PokerPoint.get_cards_max_order(self._banker)
            player_max_order = PokerPoint.get_cards_max_order(self._player)
            if banker_max_order > player_max_order:
                winstate += angel_paytable.combine_winstate(angel_mainbet_banker,angel_odds_1)
            else:
                winstate += angel_paytable.combine_winstate(angel_mainbet_player,angel_odds_1)

        logging.info(winstate)
        return winstate

    def check_sidebet(self):
        banker_point = PokerPoint.get_newnew_point(self._banker)
        player_point = PokerPoint.get_newnew_point(self._player)

        winstate = ""
        if banker_point == 7 or banker_point == 8 or banker_point == 9:
            winstate += angel_paytable.combine_winstate(angel_sidebet_bigangel_banker,angel_odds_2)
        elif banker_point == 10: 
            winstate += angel_paytable.combine_winstate(angel_sidebet_perfect_banker,angel_odds_3)

        if player_point == 7 or player_point == 8 or player_point == 9:
            winstate += angel_paytable.combine_winstate(angel_sidebet_bigangel_player,angel_odds_2)
        elif player_point == 10:
            winstate += angel_paytable.combine_winstate(angel_sidebet_perfect_player,angel_odds_3)
        return winstate

    def check_result(self):
       
        winstate = self.check_five_wawa()

        if winstate == "":
            winstate = self.check_four_of_a_kind()
            if winstate == "":
                winstate = self.check_newnew_point()

        sidebet = self.check_sidebet()
        if sidebet != "":
            winstate += sidebet
       
        msg = dict()
        msg['winstate'] = winstate
        msg['paytable'] = angel_paytable.paytable(winstate)
        msg['message_type'] = MSG_TYPE_ROUND_INFO
        self.publish(msg)


def main():
    #core = PerfectAngel()
    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage) 
   
    parser.add_option("-a", "--arm", action="store_true", default=False)
    parser.add_option("-g", "--game" ,default=1,type=int)
    (options, args) = parser.parse_args()


    if options.arm == True:
        print "options.arm True"
        core = inject(PerfectAngel, witharm = True,gametype = options.game)
    else:
        print "options.arm False"
        core = inject(PerfectAngel, witharm = False, gametype = options.game)

    print type(core)

    core.start()

if __name__ == '__main__':
    
    main()
 

