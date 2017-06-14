odd_split = "|"
zone_split = "_"

#betzone
Baccarat_banker = 0
Baccarat_player = 1
Baccarat_tie = 2
Baccarat_banker_pair = 3
Baccarat_player_pair = 4

#odds
ba_odds_0 = 0
ba_odds_095 = 1
ba_odds_1 = 2
ba_odds_8 = 3
ba_odds_11 = 4

ba_odds = {
            "0": {"odds": 0},
            "1":{"odds":1.95},
            "2": {"odds": 2},
            "3":{"odds":12},
            "4":{"odds":9},
          }

def split_symbol():
    return [zone_split,odd_split]

def bet_zone():
    return [0,1,2]

def paytable(winstate):
    winzone = winstate.split(zone_split)[:-1]

    for winlist in winzone:
        paytable = [0] * (Baccarat_player_pair+1)

    for winlist in winzone:
        info = winlist.split(odd_split)
        betzone = int(info[0])
        odds = ba_odds[info[1]]
        if betzone == Baccarat_tie:
            paytable[Baccarat_banker] = 1
            paytable[Baccarat_player] = 1
            
        paytable[betzone] = odds["odds"]
    return paytable

def combine_winstate(betZone,odds):
    return str(betZone) + odd_split + str(odds) +zone_split
