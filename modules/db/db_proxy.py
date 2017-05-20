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
        new_json.update(json_msg)

        json_data = self.get(key)
        if json_data != None:
            db_json_data = json.loads(json_data)
            new_json['for_db'] = db_json_data['for_db']
        else:
            new_json['for_db'] = json_msg['for_db']
        
        self._module.save(key,json.dumps(new_json))

    def update(self,json_msg):
        key = json_msg['key']
        new_json = dict()
        new_json.update(json_msg)
        self._module.save(key,json.dumps(new_json))

    def create_game(self,player,module,room):
        game = dict()
        game['creater'] = player
        game['module'] = module
        game['room'] = room
        self._module.save( module + "_" + room,json.dumps(game))

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

