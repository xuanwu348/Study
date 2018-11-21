import threading
from multiprocessing import Process
import time

lock = threading.Lock()

def run(info_list, n):
    try:
        lock.acquire()
        info_list.append(n)
        print("%s\n" % info_list)
    finally:
        lock.release()

if __name__ == "__main__":
    info = []
    for i in range(10):
        p = Process(target=run, args=(info, i))
        p.start()
        p.join()
    time.sleep(1)
    print("-----------threading--------------")
    for i in range(10):
        p = threading.Thread(target=run, args=(info,i))
        p.start()
        p.join()
