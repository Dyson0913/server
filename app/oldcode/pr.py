import tornado.ioloop
import tornado.web

db = "mydb"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello,world")

class StoryHandler(tornado.web.RequestHandler):
    def initialize(self,db):
        print "init %s" % db 
        self.db = db

    def get(self,story_id):
        self.write("this is story %s" % story_id)


def make_app():
    return tornado.web.Application([
        (r"/" ,MainHandler),
        (r"/story/([0-9]+)",StoryHandler,dict(db=db))
    ])

if __name__ == "__main__":
   app =make_app()
   app.listen(8888)
   tornado.ioloop.IOLoop.current().start()
