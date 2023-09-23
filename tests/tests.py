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
    
    def testSummary(self):
        from utils.conversion_parse import Summary, SL
        s = Summary('hi')
        self.assertEqual(s.txt, [{'txt': 'hi', 'lvl': 0}])
        s = Summary('`hi`')
        self.assertEqual(s.txt, [{'txt': 'hi', 'lvl': 1}])
        s = Summary('``hi``')
        self.assertEqual(s.txt, [{'txt': 'hi', 'lvl': 2}])
        s = Summary(SL('hi', 99))
        self.assertEqual(s.txt, [{'txt': 'hi', 'lvl': 99}])
        s = Summary('`hi`hi again')
        self.assertEqual(s.txt, [{'txt': 'hi', 'lvl': 1}, {'txt': 'hi again', 'lvl': 0}])
        s = Summary('`hi```bye``hi again')
        self.assertEqual(s.txt, [{'txt': 'hi', 'lvl': 1}, {'txt': 'bye', 'lvl': 2}, {'txt': 'hi again', 'lvl': 0}])
        s = Summary('%s%s%s' % (SL('qqqq', 4), SL('qqqqq', 5), SL('zzz', 3)))
        self.assertEqual(s.txt, [{'txt': 'qqqq', 'lvl': 4}, {'txt': 'qqqqq', 'lvl': 5}, {'txt': 'zzz', 'lvl': 3}])
        
        s = Summary('`hi~`hi again')
        self.assertEqual(s.txt, [{'txt': 'hi~', 'lvl': 1}, {'txt': 'hi again', 'lvl': 0}])
        self.assertEqual(s.get(0), 'hi hi again')
        self.assertEqual(s.get(1), 'hi')
        self.assertEqual(s.get(2), '')

        s = Summary('`hi hi hi```~bye bye~``hi')
        self.assertEqual(s.get(0), 'hi hi hi bye bye hi')
        self.assertEqual(s.get(1), 'hi hi hi bye bye')
        self.assertEqual(s.get(2), 'bye bye')
        self.assertEqual(s.get(3), '')

        s = Summary('(`loves-life`|``optimist``)')
        self.assertEqual(s.get(0), 'loves-life')
        self.assertEqual(s.get(1), 'loves-life')
        self.assertEqual(s.get(2), 'optimist')
        self.assertEqual(s.get(3), '')
    
        s = Summary(r'hi :\) \\') # excessive use of backslash because of python's string formatting, so use 'r' instead
        self.assertEqual(s.get(0), 'hi :) \\')

        s = Summary('```Grapefruit`````:`` (`loves-life`|``:`````~optimist```)')
        self.assertEqual(s.get(0), 'Grapefruit: loves-life')
        self.assertEqual(s.get(1), 'Grapefruit:loves-life')
        self.assertEqual(s.get(2), 'Grapefruit: optimist')
        self.assertEqual(s.get(3), 'Grapefruit optimist')
        self.assertEqual(s.get(4), '')
    
    def testKnowledge(self):
        from utils.conversion_parse import Knowledge, Summary
        K = Knowledge('Grapefruit')
        K.add_clause(is_adjs='kind/good')
        self.assertEqual(K.get(), 'Grapefruit is kind and good.')
        K.add_clause(is_a='dragon')
        self.assertEqual(K.get(), 'Grapefruit is a kind and good dragon.')
        K.add_clause(is_a='cat')
        self.assertEqual(K.get(), 'Grapefruit is a kind and good cat.') # replaces last is_a
        K.add_clause(who='loves to dance/reads lots/has a happy life')
        self.assertEqual(K.get(), 'Grapefruit is a kind and good cat who loves to dance, reads lots and has a happy life.')


if __name__ == '__main__':
    unittest.main()