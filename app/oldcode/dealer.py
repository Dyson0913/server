import logging

class dealer(object):

    def __init__(self,settler):
        self._bet_info = list()
        self.settler = settler

    def new_bet(self, player, amount, bet_type):
        new_bet = {"amount": amount, "bet_type": bet_type}

        player_bet_info = {"player": player, "bet_info": [new_bet]}
        if len(self._bet_info) == 0:
            self._bet_info.append(player_bet_info)
            return True

        for player_bet in self._bet_info:
            if player_bet["player"] == player:
                for bet in player_bet["bet_info"]:
                    if bet["bet_type"] == bet_type:
                        bet["amount"] = amount
                        return True
                player_bet["bet_info"].append(new_bet)
                return True
            
        self._bet_info.append(player_bet_info)
        return True

    def get_player_bet(self, player):
        total_bet = 0
        for player_bet in self._bet_info:
            if player_bet["player"] == player:
                for bet in player_bet["bet_info"]:
                    total_bet += bet["amount"]

        return total_bet

    def update_credit(self):
        for player_bet in self._bet_info:
            total_amount = self.get_player_bet(player_bet["player"])
            player_bet["player"].updata_credit(-total_amount)

    def settle(self, win_type):
        for player_bet in self._bet_info:
            logging.info(player_bet)
            total_amount = self.get_player_settle(
                player_bet["player"],
                win_type)
            player_bet["player"].updata_credit(total_amount)

    def get_db_settle(self,player):
        for player_bet in self._bet_info:
            if player_bet["player"] == player:
                if 'db_info' in player_bet:
                    return player_bet["db_info"]
                else:
                    return None

    def get_player_settle(self, player, win_type):
        return self.settler.get_player_settle(self,player,win_type)

    #for unit test
    def bet_len(self,player):
        for player_bet in self._bet_info:
            if player_bet["player"] == player:
                return  len(player_bet["bet_info"])

    #for unit test
    def betinfo_len(self):
        return len(self._bet_info)

    def clean_bet(self):
        del self._bet_info[:]
