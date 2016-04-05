import urllib
import datetime
from tornado import httpclient
import json

def http_query(query_cmd,name,pw,balance):
    http_client = httpclient.HTTPClient()

    response = None
    time = None
    if query_cmd == "login":
        time = datetime.datetime.now()
        request = get_acc(name,pw)
    elif query_cmd == "get_credit":
        request = get_credit(name,pw)
    elif query_cmd == "write_back":
        request = update_credit(name,pw,balance)

    try:
#        body = urllib.urlencode(request)
        json_msg = json.dumps(request)
        time = datetime.datetime.now()
        httpresponse = http_client.fetch("http://slot.hq-game.com/api/index.php", method='POST',body=json_msg)
        response =  httpresponse.body

    except httpclient.HTTPError as e:
        print("Error: " + str(e))
    except Exception as e:
        print("Error: " + str(e))
    if query_cmd == "login":
        print datetime.datetime.now() - time
#    print "get"
#    print response
    return json.loads(response)

def get_acc(name,pw):
    request = dict()
    request['action'] = 1
    paras = dict()
    paras['user'] = name
    paras['pwd'] = pw
    request['paras'] = paras
    return request

def get_credit(name,pw):
    request = dict()
    request['action'] = 2
    paras = dict()
    paras['user'] = name
    paras['pwd'] = pw
    request['paras'] = paras
    return request

def update_credit(name,pw,balance):
    request = dict()
    request['action'] = 3
    paras = dict()
    paras['user'] = name
    paras['pwd'] = pw
    paras['balance'] = balance
    request['paras'] = paras
    return request

def main():
    http_query("login","test","test",0)

if __name__ == "__main__":
    main()

