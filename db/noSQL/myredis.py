import redis
#print dir(redis)
# "redis": {"host":"localhost","port":6379, "db":0},


# conn_info = self._redis_conn.get(msg[KEY_GAME_ID])
#self._redis_conn.set(msg[KEY_GAME_ID], json.dumps(conn_info))
def main():

#    redis_server = redis.StrictRedis(host='localhost', port=6379,password='dyson')
    redis_server = redis.StrictRedis(host='52.193.112.227', port=6379,password='dyson')
#    redis_server.flushall()

    redis_server.set("redis_test","maintest")
    if redis_server.get("redis_test") == "maintest":
         print "ok"
    else:
         print "not ok"

if __name__ == "__main__":

    main()
