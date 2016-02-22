

import socket
import sys
from ball5enc import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 5030)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)


Key = [ 0x6A, 0x6B, 0x33, 0x16, 0x86, 0x62, 0x89, 0x71, 0x19, 0x39, 0x7C, 0x52, 0xF2, 0x1B, 0x88, 0xFC ]
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                dec_command = decrypt_command(data, Key)

                connection.sendall(dec_command)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
                                                            
    finally:
        # Clean up the connection
        connection.close()



