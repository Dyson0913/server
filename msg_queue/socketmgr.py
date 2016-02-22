

class socketmgr(object):

      client = {}

      @staticmethod
      def add(client_id,cls):

          if socketmgr.client.has_key(client_id) == False:
               socketmgr.client[client_id] = cls

          socketmgr.show_all()
      
      @staticmethod
      def get(client_id):

          if socketmgr.client.has_key(client_id) == False:
              return None
          else:
              return socketmgr.client[client_id]

      @staticmethod
      def show_all():
          print "show_all"
          for client in socketmgr.client:
              print client



def main():
    socketmgr.add(1,"ss")
    socketmgr.add(2,"dd")

    if socketmgr.get(1) == "ss" and socketmgr.get(2) == "dd":
        print "main test ok"
    else:
        print "main test wrong"
 

if __name__ == "__main__":
    main()

