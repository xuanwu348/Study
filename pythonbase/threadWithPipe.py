import threading
import os
import time
from multiprocessing import Pipe


r, w = Pipe()


def runW_CMD():
    
    
    while True:
        time.sleep(1)
        print("in thread")
        w.send("teste......................")

t = threading.Thread(target=runW_CMD)
t.start()

while 1:
    
    time.sleep(1)
    print("in main")
    print(r.recv())
    
t.join()
