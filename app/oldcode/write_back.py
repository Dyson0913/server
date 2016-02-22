import zmq
import urllib
import datetime
from tornado import httpclient
import json

def account_verity():
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.linger = 0
    socket.bind("tcp://127.0.0.1:6666")
   
    http_client = httpclient.HTTPClient()
    response = None;
    while True:
        msg = socket.recv_json()
        print msg
        if msg:
            try:
                AppToken = "535942062|7f415b11056cf408b0cd87ceb7020466";
                if msg['Action'] == 'putGameResult':
                    msg['AppToken'] = AppToken
                elif msg['Action'] == 'putOrderInfo':
                    msg['AppToken'] = AppToken

                if msg['auth'] == False:
                    fakemsg = dict()
                    fakemsg['error'] = 0
                    data = dict()

                    if msg['Action'] == 'putGameResult':
                        data['ResultID'] = 'fakeID'
                    elif msg['Action'] == 'putOrderInfo':
                        data['OrderID'] = 'fakeID'
                    fakemsg['data'] = data
                    response = json.dumps(fakemsg)
                else:
                    del msg['auth']
                    if msg['Action'] == 'putOrderInfo':
                        msgj = json.dumps(msg["BetList"])
                        msg["BetList"] = msgj

                    post_data = msg
                    body = urllib.urlencode(post_data)
                    httpresponse = http_client.fetch("http://sooq.us.to/v1.0/", method='POST',body=body)
                    response =  httpresponse.body

                
            except httpclient.HTTPError as e:
                # HTTPError is raised for non-200 responses; the response
                # can be found in e.response.
                print("Error: " + str(e))
            except Exception as e:
                # Other errors are possible, such as IOError.
                print("Error: " + str(e))
            print response
            socket.send(response)
    #http_client.close()

def main():
    account_verity()


if __name__ == "__main__":
    main()


