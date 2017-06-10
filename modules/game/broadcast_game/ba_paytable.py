odd_split = "|"
zone_split = "_"

#betzone
Baccarat_banker = 0
Baccarat_player = 1
Baccarat_tie = 2
Baccarat_banker_pair = 3
Baccarat_player_pair = 4

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

def split_symbol():
    return [zone_split,odd_split]

def bet_zone():
    return [0,1,2]

def paytable(winstate):
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

def combine_winstate(betZone,odds):
    return str(betZone) + odd_split + str(odds) +zone_split
