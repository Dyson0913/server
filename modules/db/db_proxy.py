
import sys
sys.path.append("noSQL/")

import myredis
from myredis import *


class db_proxy(object):

    def __init__(self,host,port,pw):

        self._module = redis_db(host,port,pw)
        print "redis listen in {0}:{1}".format(host,port)

    def save(self,json_msg):
        key = json_msg['client_id']
        del json_msg['client_id']
        self._module.save(key,json_msg)

    def get(self,json_msg):
        key = json_msg['client_id']
        return self._module.get(key)

    def clean(self,client_id):
        self._module.clean(client_id)

def main():
    # create any kind db module you want
    #data = config_parser()

    db = db_proxy('127.0.0.1',6379,None)
    while (True):
        pass

if __name__ == "__main__":
    main()

