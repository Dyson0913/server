import socket
import sys
from ball5enc import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5030)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

Key = [ 0x6A, 0x6B, 0x33, 0x16, 0x86, 0x62, 0x89, 0x71, 0x19, 0x39, 0x7C, 0x52, 0xF2, 0x1B, 0x88, 0xFC ]
while(1):

    
    # Send data
    #message = 'This is the message.  It will be repeated.'
    message = raw_input("Command \n")
    enc_message = encrypt_command(message, Key)

    print >>sys.stderr, 'sending "%s"' % enc_message
    

    sock.sendall(enc_message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
        
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

print >>sys.stderr, 'closing socket'
sock.close()
