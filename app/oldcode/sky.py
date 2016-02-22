import socket
import sys
import time
import threading
from ball5enc import *

#Key = [ 0x6A, 0x6B, 0x33, 0x16, 0x86, 0x62, 0x89, 0x71, 0x19, 0x39, 0x7C, 0x52, 0xF2, 0x1B, 0x88, 0xFC ]
Key = [ 0x03, 0x2C, 0x23, 0x2A, 0xCB, 0x85, 0x76, 0xE2, 0x85, 0x93, 0x4B, 0x80, 0xE1, 0x5C, 0x48, 0xE1 ]


def main():

    sock_reset = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reset_address=('220.132.215.90', 5031)
    print >>sys.stderr, 'connecting to %s port %s' % reset_address

    sock_reset.connect(reset_address)


    time.sleep(5)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Connect the socket to the port where the server is listening
    server_address = ('220.132.215.90', 5032)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    recv_thread = threading.Thread(target=recv_func,args=(sock,))
    recv_thread.daemon = True
    recv_thread.start()


    while(1): 
        # Send data
        #message = 'This is the message.  It will be repeated.'
        message = raw_input("Command \n")
        enc_message = encrypt_command(message, Key)

        print >>sys.stderr, 'sending "%s"' % enc_message
    

        sock.sendall(enc_message)

        # Look for the response
#        amount_received = 0
#       amount_expected = len(message)
        
#while amount_received < amount_expected:
#            data = sock.recv(16)
#            amount_received += len(data)
#            print >>sys.stderr, 'received "%s"' % data

#            dec_command = decrypt_command(data, Key)

#            print >>sys.stderr, 'received dec_command %s"' % dec_command

    print >>sys.stderr, 'closing socket'
    sock.close()


def recv_func(sock):
    amount_received = 0
    count = 0
    buf = ""
    while True:
        data = sock.recv(1)
        # if len(data) == 0:
        #count += 1
        #if count % 100 == 0:
        #print len(data), type(sock)
        #print >>sys.stderr, 'received "%s" len:%d' % (data,len(data))
        if data == ";":
            data_len = int(buf)
            enc_data = sock.recv(data_len)
            dec_command = decrypt_command(enc_data, Key)
            print >>sys.stderr, 'received dec_command %s"' % dec_command
            buf=""
        else:
            buf += data

if __name__ == '__main__':
    main()

