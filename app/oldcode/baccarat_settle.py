from collections import *
from ba_paytable import *
import ba_paytable

def get_player_settle(dealer, player, win_type):
    paytable = ba_paytable.paytable(win_type)
    total_amount = 0
    msg = list()
    for player_bet in dealer._bet_info:
        if player_bet["player"] == player:
            for bet in player_bet["bet_info"]:
                amount =  bet["amount"] * paytable[bet["bet_type"]]
                total_amount += amount

                betlist = dict()
                betlist["BetAmount"] = bet["amount"]
                betlist["BetItem"] = bet["bet_type"]

                win = "W"
                if amount == 0:
                    win = "L"
                else:
                    if win_type == Baccarat_tie and bet["bet_type"] != win_type:
                        win = "T"

                betlist["Winloss"] = amount
                betlist["BetStatus"] = win
                msg.append(betlist)

            player_bet["db_info"] = msg
    return total_amount

