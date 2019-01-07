class Single_c(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Single_c, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, statusNumber):
        self.statusNumber = statusNumber

if __name__ == "__main__":
    A = Single_c(2)
    B = Single_c(5)
    print(id(A),id(B))
    print(A.statusNumber)
    print(B.statusNumber)
        
