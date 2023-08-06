# To import a module in different package
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from src.divide.divide_by_five import divide_five
# from src/divide/divide_by_five.py (module), we import function divide_five()

class TestDivideByFive(unittest.TestCase):
   def test_divide_by_five(self):
      self.assertEqual(divide_five(15), 3)


unittest.main() # The unittest.main() is instantiated to run all our tests.
