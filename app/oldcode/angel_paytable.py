odd_split = "|"
zone_split = "_"


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

def split_symbol():
    return [zone_split,odd_split]

def bet_zone():
    return [1,2,3,4,5,6]

def paytable(winstate):
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

