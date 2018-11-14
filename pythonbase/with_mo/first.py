#encoding:utf-8

class DummyResource:
    def __init__(self, tag):
        self.tag = tag
        print("\033[32mResource [%s]\033[0m" % tag)

    def __enter__(self):
        print("\033[33m[Enter %s]: Allocate resource." % self.tag)
        return self

    def fun_test(self):
        print("[Fun_test] %s" % self.tag)

    def __exit__(self, exc_type, exc_value, exc_trb):
        print(exc_type, exc_value, exc_trb)
        print("\033[31m[Exit %s]: Free resource.\033[0m" % self.tag)
        if exc_trb is None:
            print("\033[31m[Exit %s]: Exited without exception.\033[0m" % self.tag)
        else:
            print("\033[31m[Exit %s]: Exited with exception raised." % self.tag)
            return False    #transfer the exception to the upper.
            #return True      #ignore the exception.


#python first.py > run_result.log 2>&1

with DummyResource("Normal"):
    print("hererere.......")
    #raise IndexError("sssssssss")
print("*" * 25)
with DummyResource("Normal") as f:
    f.fun_test()
    print("hererere.......")
    #raise IndexError("sssssssss")

print("*" * 25)
with DummyResource("Normal"):
    print("hererere.......")
    raise IndexError("sssssssss")

