def singleton(cls):
    instance = cls()
    instance.__call__ = lambda : instance
    return instance

@singleton
class test_:
    x = 100

if __name__ == "__main__":
    print(test_() is test_() is test_)
    test_.x = 50
    print(test_.x == test_().x)
