#encoding:utf-8
from contextlib import closing

"""
class closing(object):
    def __init__(self, thing):
        self.thing = thing
    def __enter__(self):
        return self.thing
    def __exit__(self, *exc_info):
        self.thing.close()

   the object which will be contained in contextmanager should provide a close() function 
"""
class ClosingDemo(object):
    def __init__(self):
        self.acquire()
    def acquire(self):
        print("Acquired resource")
    def free(self):
        print("Clean up any resource acquired.")
    def close(self):
        self.free()

if __name__ == "__main__":
    with closing(ClosingDemo()):
        print("Using resource")
