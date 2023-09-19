import unittest

import os, sys
if os.getcwd().endswith('tests'): # set folder to one above
    newpath = os.path.abspath(os.path.join(os.getcwd(), '../'))
    os.chdir(newpath)
sys.path.append(os.getcwd()) # and make sure we can access all stuff as if from folder above

class TestConversationParser(unittest.TestCase):
    def test_kwarg_parser(self):
        from utils.conversion_parse import parseKWs
        with self.assertRaises(ValueError) as cm:
            parseKWs({'hi': 'bye'}, ['hello'])
        self.assertEqual(str(cm.exception), 'Unknown kwarg "--hi"\nAvaliable args: "--hello"')
        with self.assertRaises(ValueError) as cm:
            parseKWs({'hihihi': 'hello'}, ['hello', 'goodbye'])
        self.assertEqual(str(cm.exception), 'Unknown kwarg "--hihihi"\nAvaliable args: "--hello --goodbye"')

        parseKWs({'hello': 'bye'}, ['hello'])
        parseKWs({'hi': 'bye'}, ['hi', 'cyas'])
        parseKWs({'hello': 'bye', 'byes': 'bye'}, ['hello', 'byes'])
        with self.assertRaises(ValueError) as cm:
            parseKWs({'jello': 'cat'}, ['jello', 'goodbye'], ['goodbye'])
        self.assertEqual(str(cm.exception), 'Missing required kwargs: "--goodbye"')
        with self.assertRaises(ValueError) as cm:
            parseKWs({'hello': 'bye'}, ['hello', 'goodbye'], [('goodbye', 'hi')])
        self.assertEqual(str(cm.exception), 'Missing required kwargs: "(--goodbye or --hi)"')

        parseKWs({'hello': 'bye'}, ['hello', 'goodbye'], [('goodbye', 'hello')])
        parseKWs({'goodbye': 'bye'}, ['hello', 'goodbye'], [('goodbye', 'hello')])

if __name__ == '__main__':
    unittest.main()