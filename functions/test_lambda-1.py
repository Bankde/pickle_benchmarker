#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Lambda expression
- Simple lambda expression
- Function that return lambda
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from functools import reduce

def function_return_lambda(c):
    d = c*2
    return lambda a: a*d

class Test(helper.PickleTest):
    def test_lambda(self):
        # According to PEP8, we do not name the lambda expressions
        self.assertEqual(list(filter(lambda s: s.isupper() or s.islower(), ["hello", "wOrlD", "HELLO"])), ["hello", "HELLO"])
        self.obj['l1'] = self.dumps(lambda s: s.isupper() or s.islower())
        self.assertEqual(list(map(lambda a: a**2, [1,2,3,5,7])), [1,4,9,25,49])
        self.obj['l2'] = self.dumps(lambda a: a**2)
        self.assertEqual(reduce(lambda x,y: x*y, [1,2,3,5,7], 1), 210)
        self.obj['l3'] = self.dumps(lambda x,y: x*y)

    def test_function_return_lambda(self):
        self.assertEqual(function_return_lambda(17)(3), 102)
        self.obj['f1'] = self.dumps(function_return_lambda)
        self.obj['l1'] = self.dumps(function_return_lambda(17))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()