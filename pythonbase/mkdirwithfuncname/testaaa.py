import unittest
import inspect
from datas import mkdir

class Testaa(unittest.TestCase):
    def test_aa(self):
        mkdir()

    def test_bb(self):
        mkdir()
    
if __name__ == "__main__":
    unittest.main()
