odd_split = "|"
zone_split = "_"

#betzone
bigwin_banker = 1
bigwin_player = 2

#odds
big_odds_1000 = 1
big_odds_100 = 2
big_odds_40 = 3
big_odds_10 = 4
big_odds_6 = 5
big_odds_4 = 6
big_odds_1 = 7
big_odds_0 = 8


big_odds = {
           "1":{"odds":1001},
           "2":{"odds":101},
           "3":{"odds":41},
           "4":{"odds":11},
           "5":{"odds":7},
           "6":{"odds":5},
           "7":{"odds":2},
           "8":{"odds":0}
          }

def split_symbol():
    return [zone_split,odd_split]

def bet_zone():
    return [1,2]

def paytable(winstate):
    winzone = winstate.split(zone_split)[:-1]

    for winlist in winzone:
        info = winlist.split(odd_split)
        if int(info[1]) <= big_odds_4:
            odds = big_odds[info[1]]
            paytable = [odds["odds"]] * (bigwin_player+1)
        else:
            paytable = [0] * (bigwin_player+1)

    for winlist in winzone:
        info = winlist.split(odd_split)
        betzone = int(info[0])
        odds = big_odds[info[1]]
        paytable[betzone] = odds["odds"]
    return paytable

def combine_winstate(betZone,odds):
    return str(betZone) + odd_split + str(odds) +zone_split
