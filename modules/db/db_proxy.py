import sys
sys.path.append("noSQL/")

import json
import myredis
from myredis import *


class db_proxy(object):

    def __init__(self,host,port,pw):

        self._module = redis_db(host,port,pw)
        print "redis listen in {0}:{1}".format(host,port)

    def save(self,json_msg):
        key = json_msg['key']
 
        new_json = dict() 
        new_json['state'] = json_msg['state']
        new_json['key'] = json_msg['key']

        json_data = self.get(json_msg)
        if json_data != None:
            db_json_data = json.loads(json_data)
            new_json['for_db'] = db_json_data['for_db']
        else:
            new_json['for_db'] = json_msg['for_db']
        
        self._module.save(key,json.dumps(new_json))

    def create_game(self,room_name,player):
        game = dict()
        game['creater'] = player
        self._module.save(room_name,json.dumps(game))

    def get(self,key):

        if key == None:
           print "no key return None"
           return None

        return self._module.get(key)

    def clean(self,client_id):
        self._module.clean(client_id)

def main():
    # create any kind db module you want
    db = db_proxy('127.0.0.1',6379,None)
    while (True):
        pass

if __name__ == "__main__":
    main()

