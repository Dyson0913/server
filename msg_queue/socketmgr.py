

class socketmgr(object):

      client = {}
      val_to_key ={}

      @staticmethod
      def add(client_id,client):

          if socketmgr.client.has_key(client_id) == False:
               socketmgr.client[client_id] = client
               socketmgr.val_to_key[client] = client_id

          socketmgr.show_all()


      @staticmethod
      def remove(client):
          if socketmgr.val_to_key.has_key(client):
              client_id = socketmgr.val_to_key[client]
              del socketmgr.client[client_id]
              del socketmgr.val_to_key[client]
          
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
    socketmgr.add(3,"cc")

    socketmgr.remove("cc")

    if socketmgr.get(1) == "ss" and socketmgr.get(2) == "dd":
        print "main test ok"
    else:
        print "main test wrong"
 

if __name__ == "__main__":
    main()

