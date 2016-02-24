import uuid

my_globals = {'client':{},'val_to_key':{},'name':None}


#      client = {}
#      val_to_key ={}
#      name = None
#      @classmethod
def add(client_id,client):

    if my_globals['client'].has_key(client_id) == False:
        if len(my_globals['client']) ==0:
            my_globals['name'] = uuid.uuid1().hex

        my_globals['client'][client_id] = client
        my_globals['val_to_key'][client] = client_id

    show_all()

def remove(client):
    if my_globals['val_to_key'].has_key(client):
        client_id = my_globals['val_to_key'][client]
        del my_globals['client'][client_id]
        del my_globals['val_to_key'][client]
          
    show_all()
      
def get(client_id):

    if my_globals['client'].has_key(client_id) == False:
        return None
    else:
        return my_globals['client'][client_id]

def show_all():
    print "show_all %s " % my_globals['name']
    for client in my_globals['client']:
        print client
    print "---"


def main():
    add(1,"ss")
    add(2,"dd")
    add(3,"cc")

    remove("cc")

    if get(1) == "ss" and get(2) == "dd" and get(3) == None:
        print "main test ok"
    else:
        print "main test wrong"
 

if __name__ == "__main__":
    main()

