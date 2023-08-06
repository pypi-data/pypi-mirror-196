# To import a module in different package
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import os
import sys
sys.path.insert(0, os.getcwd())

import unittest
from src.multiply.multiply_by_five import multiply_five
# from src/multiply/multiply_by_five.py (module), we import function multiply_five()
class TestMultiplyByFive(unittest.TestCase):
	def test_multiply_by_five(self):
		self.assertEqual(multiply_five(3), 15)

unittest.main() # The unittest.main() is instantiated to run all our tests.