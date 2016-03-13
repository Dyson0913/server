import redis
#print dir(redis)

class redis_db(object):

    def __init__(self,host,port,password):

        self._db = redis.StrictRedis(host=host, port=port,password=password)

    def save(self,key,json_msg):
        self._db.set(key,json_msg)

    def get(self,key):
        return self._db.get(key)

    def clean(self,key):
        self._db.delete(key)

def main():

    myredis = redis_db("52.193.112.227",6379,None)
#    redis_server.flushall()
    myredis.save("redis_test","test")
    myredis.save("redis_test2","test2")
    if myredis.get("redis_test") == "ntest":
         print "ok"
         myredis.clean("redis_test2")
    else:
         print "not ok"

if __name__ == "__main__":

    main()
