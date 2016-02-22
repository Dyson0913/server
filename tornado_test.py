#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# ddLicensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.ioloop
import tornado.options
import tornado.websocket
from tornado.options import define, options

import os.path
import json

#game 
import sys
sys.path.append("msg_queue/")
sys.path.append("msg_queue/zmqModual/")
sys.path.append("app/")
from requester import *

import uuid

define("port", default=7000, help="run on the given port", type=int)

#zmq ioloop conflact with tornado ioloop,need call this asap befort
#tonado ioloop
# reference https://pyzmq.readthedocs.org/en/latest/eventloop.html
ioloop.install()

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
        return True

#    @gen.coroutine
    def open(self,token):
        wshandler.cnt = wshandler.cnt+1
        print wshandler.cnt

        #worker & client send to back
        msg = dict()
        msg['id'] = wshandler.cnt
        msg['cmd'] = "login"
        msg['client'] = self
        msg['client_id'] = uuid.uuid1().hex
        wshandler.sender.send(msg)

        #self.write_message(msg)
    def on_close(self):
        print "close"
        #TODO leaveing
        msg = dict()
        msg['id'] = wshandler.cnt
        msg['cmd'] = "close"
        msg['client'] = self
        wshandler.sender.send(msg)

    def on_message(self, message):
        print message

        #TODO client res
#        wshandler.send.send



def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
   
    wshandler.sender = msg_sender(zmq_request("7788"))

    print tornado.ioloop.IOLoop.instance()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
