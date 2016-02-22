from collections import *
import big_paytable

def get_player_settle(dealer, player, win_type):
    paytable = big_paytable.paytable(win_type)
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

                betlist["Winloss"] = amount
                betlist["BetStatus"] = win
                msg.append(betlist)

            player_bet["db_info"] = msg
    return total_amount
