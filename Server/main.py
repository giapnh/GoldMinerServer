__author__ = 'Nguyen Huu Giap'
from socket import *
import threading
import thread


def handle_client(c):
    while 1:
        print "received"
        c.recv(1000)
        print "received"
    pass

s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost", 9999))
# s.setblocking(0)
s.listen(5)
while True:
    print "waiting"
    c, a = s.accept()
    print "Received connection from " + str(a)
    # t = threading.Thread(target=handle_client, args=(c,))
    t = thread.start_new_thread(handle_client, (c, ))
