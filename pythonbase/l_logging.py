import logging
from multiprocessing import Pool
from os import getpid

def runs_in_subprocess():
    logging.info("I am in the child, with PID {}".format(getpid()))

if __name__ == "__main__":
    logging.basicConfig(format="sssss %(message)s", level=logging.DEBUG)
    logging.info("I am in the parent, with PID {}".format(getpid()))
    """
    with version > 3.2 can use as below
    with Pool(processes = 4) as pool:
        pool.apply(.......)
    otherwise prompt AttributeError: no __exit__
    """
    pool = Pool(processes = 4)
    pool.apply(runs_in_subprocess)
    pool.terminate()
