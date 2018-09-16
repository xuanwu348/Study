from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x * x

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        print(pool.map(f, range(10)))

        for i in pool.imap_unordered(f, range(10)):
            print(i)

        res = pool.apply_async(f,(20,))
        print(res.get(timeout=1))

        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("Occurred a multiprocessing.TimeOutError")
