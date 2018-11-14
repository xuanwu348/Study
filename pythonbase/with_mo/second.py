from contextlib import contextmanager

@contextmanager
def demo(): 
    #The decorated function can generate only on value, otherwise raise RuntimeError, 
    #and if the 'with' expression used 'as target', the generated value will be assign to target  
    print('[Allocate resurce]')
    print("Code before yield-statement excutes in __enter__")
    yield '*** contextmanager demo***'
    print("code after yield-statement executes in __exit__")
    print("[[Free resource]")

with demo() as value:
    print("Assigned value: %s" % value)
    raise NameError
