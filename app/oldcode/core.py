from tornado import gen, tcpclient
from tornado.ioloop import IOLoop, PeriodicCallback
import time
import sys
from ball5enc import *

Key = [ 0x03, 0x2C, 0x23, 0x2A, 0xCB, 0x85, 0x76, 0xE2, 0x85, 0x93, 0x4B, 0x80, 0xE1, 0x5C, 0x48, 0xE1 ]
tcp_client = tcpclient.TCPClient()
sock = None
tcp_main = tcpclient.TCPClient()
sock_main = None
send_count = 0

@gen.coroutine
def try_connect():
    global sock
    global tcp_client
    print "About to connect"

    try:
        sock = yield tcp_client.connect('220.132.215.90', 5031)
        print type(sock)
        print "Connected !!!"
    except Exception as e:
        print "Caught Error: %s" % e

@gen.coroutine
def main_connect():
    global sock_main
    global tcp_main

    try:
        sock_main = yield tcp_main.connect('220.132.215.90', 5032)
        print "Main Connected !!!"
    except Exception as e:
        print "Main Caught Error: %s" % e

def on_body(data):
        dec_command = decrypt_command(data, Key)
        print "on_body : %s" % dec_command

def on_headers(data):
    #print data
    data_len = int(data[:-1])
    #print data, data_len
    sock_main.read_bytes(data_len, on_body)

def main_recv():
    amount_received = 0
    count = 0
    buf = ""
    if sock_main == None:
        return
    #try:
    if sock_main.reading() != True:
        sock_main.read_until(";", on_headers)

    #except Exception as e:
    #    print "main_recv error: %s" % e
    #sock_main.read_bytes(1)
    #print data
    #while True:
    #    data = sock_main.read_bytes(1)
    #    print data
    #    if len(data) == 0:
    #        break
        #count += 1
        #if count % 100 == 0:
        #print len(data), type(sock)
        #print >>sys.stderr, 'received "%s" len:%d' % (data,len(data))
    #    if data == ";":
    #        data_len = int(buf)
    #        enc_data = sock.read_bytes(data_len)
    #        dec_command = decrypt_command(enc_data, Key)
    #        print >>sys.stderr, 'received dec_command %s"' % dec_command
    #        buf=""
    #    else:
    #        buf += data

def main_send():
    global send_count
    #message = raw_input("Command \n")
    if sock_main:
    
        if send_count == 0:
            message = "0,4,2"
            send_count += 1
        else:
            message = "21,1,1"

        enc_message = encrypt_command(message, Key)

        print >>sys.stderr, 'sending "%s"' % enc_message
    
        sock_main.write(enc_message)


if __name__ == '__main__':
    try_connect()
    time.sleep(5)
    main_connect()
    recv_callback = PeriodicCallback(main_recv, 100)
    send_callback = PeriodicCallback(main_send, 10000)
    recv_callback.start()
    send_callback.start()
    IOLoop.instance().start()
