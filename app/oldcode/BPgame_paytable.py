from poker import *

odd_split = "|"
zone_split = "_"

#betzone
Baccarat_banker = 1
Baccarat_player = 2
Baccarat_tie = 3
Baccarat_banker_pair = 4
Baccarat_player_pair = 5

#odds
ba_odds_11 = 1
ba_odds_8 = 2
ba_odds_095 = 3
ba_odds_1 = 4
ba_odds_0 = 5

ba_odds = {
           "1":{"odds":12},
           "2":{"odds":9},
           "3":{"odds":1.95},
           "4":{"odds":2},
           "5":{"odds":0},
          }


def Baccarat_paytable(winstate):
    winzone = winstate.split(zone_split)[:-1]

    for winlist in winzone:
        info = winlist.split(odd_split)
	if str(Baccarat_tie) == info[0]:
            paytable = [1] * (Baccarat_player_pair+1)
            break
        else:
            paytable = [0] * (Baccarat_player_pair+1)

    for winlist in winzone:
        info = winlist.split(odd_split)
        betzone = int(info[0])
        odds = ba_odds[info[1]]
        paytable[betzone] = odds["odds"]
    return paytable


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

def Bigwin_paytable(winstate):
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

#betzone
angel_mainbet_banker = 1
angel_mainbet_player = 2
angel_sidebet_bigangel_banker = 3
angel_sidebet_bigangel_player = 4
angel_sidebet_perfect_banker = 5
angel_sidebet_perfect_player = 6

#odds
angel_odds_40 = 1
angel_odds_3 = 2
angel_odds_2 = 3
angel_odds_1 = 4
angel_odds_0 = 5

angel_odds = {
           "1":{"odds":41},
           "2":{"odds":4},
           "3":{"odds":3},
           "4":{"odds":2},
           "5":{"odds":0},
          }

def angel_paytable(winstate):
    winzone = winstate.split(zone_split)[:-1]

    paytable = [0] * (angel_sidebet_perfect_player +1)
    for winlist in winzone:
        info = winlist.split(odd_split)
        betzone = int(info[0])
        odds = angel_odds[info[1]]
        paytable[betzone] = odds["odds"]
    return paytable

def combine_winstate(betZone,odds):
    return str(betZone) + odd_split + str(odds) +zone_split
