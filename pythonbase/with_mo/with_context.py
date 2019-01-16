import os

class Sample:
    current_path = os.path.abspath(os.path.dirname(__file__))
    def __init__(self, path):
        self.path = path
        
    def __enter__(self):
        print("In __enter__()")
        os.chdir(self.path)
        print(os.getcwd())
        return self

    def f(self):
        print("Sample function")

    
    def __exit__(self, ExceptType, ExceptValue, trace):
        print("In __exit__()")
        os.chdir(Sample.current_path)
        print(os.getcwd())

with Sample(r"/home/pi/git/") as sample:
    print("Sample:%s" % sample)
    print("Do some Func in point path")
    print("in with %s " % os.getcwd())
    sample.f()

print("--" * 20)
print(os.getcwd())
