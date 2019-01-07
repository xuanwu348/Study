import threading

try:
    from synchronize import make_synchronized
except ImportError:
    def make_synchronized(func):
        func.__lock__ = threading.Lock()

        def synced_func(*args, **kwargs):
            with func.__lock__:
                return func(*args, **kwargs)

        return synced_func

class Singleton(object):
    __instance = None

    @make_synchronized
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.content = "Single instance"

def test():
    a = Singleton()
    print(id(a))

def test2():
    a1 = Singleton()
    a2 = Singleton()
    a1 .content = "change content"
    print(id(a1), id(a2))
    print(a1.content, a2.content) 

if __name__ == "__main__":
    test2()
    task = []
    for one in range(30):
        t = threading.Thread(target=test)
        task.append(t)
        t.start()
    for one in task:
        one.join()


