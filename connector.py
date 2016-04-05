#!/usr/bin/env python
#     http://www.apache.org/licenses/LICENSE-2.0

import tornado.ioloop
import tornado.options
import tornado.websocket
#from tornado.options import define, options
from tornado.httpserver import HTTPServer

import json
import uuid
import os.path

#game 
import sys
sys.path.append('modules/msg_queue')
sys.path.append('modules/msg_queue/zmqModual')

from requester import *
from config_parser import * 

#define("port", default=7000, help="run on the given port", type=int)

#zmq ioloop conflact with tornado ioloop,need call this asap befort
#tonado ioloop
# reference https://pyzmq.readthedocs.org/en/latest/eventloop.html
ioloop.install()

settings = dict(
    ssl_options = {
        "certfile":"server.crt",
        "keyfile":"server.key",
    }
)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/gamesocket/(\w+)", wshandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class wshandler(tornado.websocket.WebSocketHandler):

    cnt = 0
    sender = None

    # nginx + websocket connect to tornado default value is false for tornado 4.0+
    # override and return True let the connection success
    def check_origin(self,origin):
        print origin
        return True

   # @gen.coroutine
    def open(self,token):
        wshandler.cnt = wshandler.cnt+1
        print "cliet open %d" % wshandler.cnt

        #worker & client send to back
        msg = dict()
        msg['id'] = wshandler.cnt
        msg['module'] = "auth"
        msg['cmd'] = "login"
        msg['token'] = token
        msg['client'] = self
        msg['client_id'] = uuid.uuid1().hex
        wshandler.sender.send(msg)

        #self.write_message(msg)
    def on_close(self):
        print "close"
        msg = dict()
        msg['module'] = "auth"
        msg['cmd'] = "self_close"
        msg['client'] = self
        wshandler.sender.send(msg)

    def on_message(self,data):
        #print data
        json_msg = json.loads(data)

#        msg= dict()
#        msg['module'] = json_msg['module']
#        msg['cmd'] = json_msg['cmd']
#        msg['uuid'] = json_msg['uuid']
        wshandler.sender.send(json_msg)



def main():
#    tornado.options.parse_command_line()
    data = config_parser()
    app = Application()
    app.listen(data['port'])
 
    wshandler.sender = msg_sender(zmq_request(data))
    print tornado.ioloop.IOLoop.instance()

#    wss
#    http_server = HTTPServer(app,**settings)
#    http_server.listen(data['port'])

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
