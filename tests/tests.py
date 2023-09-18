import unittest

import os, sys
if os.getcwd().endswith('tests'): # set folder to one above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../'))
    os.chdir(newpath)
sys.path.append(os.getcwd()) # and make sure we can access all stuff as if from folder above

class TestDemo(unittest.TestCase):
    def test_bad_type(self):
        data = "banana"
        with self.assertRaises(TypeError):
            result = sum(data)
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()