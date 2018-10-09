import threading
import time

def light():
    count = 0
    while True:
        time.sleep(1)
        if count < 10:
            event.set()
            print("\033[42mGreenLight\033[0m")
        elif count < 13:
            if not event.isSet():
                event.set()
            print("\033[43mYelloLight\033[0m")
        elif count < 20:
            event.clear()
            print("\033[41mRedLight\033[0m")
        else:
            count = 0
        count += 1

def car(car_plate):
    while True:
        time.sleep(0.8)
        if event.isSet():
            print("%s car running" % car_plate)
        else:
            print("%s car is waiting" % car_plate)
            event.wait()


if __name__ == "__main__":
    event = threading.Event()
    t = []
    tt = threading.Thread(target = light)
    tt.start()
    t.append(tt)
    car1 = threading.Thread(target = car, args=("xxxxxxx1",))
    t.append(car1)
    car1.start()
    car2 = threading.Thread(target = car, args=("xxxxxxx2",))
    t.append(car2)
    car2.start()

    for tt in t:
        tt.join()


