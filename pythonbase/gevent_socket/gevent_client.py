import os
import socket
import time
import random

HOST = "localhost"
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    msg = bytes("just only a test with %s" % random.randrange(2**8,2**10),encoding="utf-8")
    #msg = bytes(input(">>:"),encoding="utf-8")
    s.send(msg)
    #time.sleep(1)
    data = s.recv(1024)
    print("receive: %s" % data.decode("utf-8"))

s.close()

