
client = {}
val_to_key ={}

def add(client_id,cli):

    if client.has_key(client_id) == False:
       client[client_id] = cli
       val_to_key[cli] = client_id

def remove(cli):
    if val_to_key.has_key(cli):
        client_id = val_to_key[cli]
        del client[client_id]
        del val_to_key[cli]
#    show_all()
      
def get(client_id):

    if client.has_key(client_id) == False:
        return None
    else:
        return client[client_id]

def show_all():
    for cli in client:
        print cli
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

