#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Simple Function
- Testing function with params
- Testing function with default params
- Testing function with inner import
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

def function_one_param(a):
    return a
def function_two_param(a,b):
    return a+b
def function_default_param(a=2):
    return a
def function_two_param_with_default_param(a,b=2):
    return a+b
def function_inner_import(arr):
    import numpy as np
    return np.argmax(arr)
class Test(helper.PickleTest):
    def test_function_param(self):
        self.assertEqual(function_one_param(5), 5)
        self.assertEqual(function_two_param(5,7), 12)
        self.obj['f1'] = self.dumps(function_one_param)
        self.obj['f2'] = self.dumps(function_two_param)

    def test_function_default_param(self):
        self.assertEqual(function_default_param(), 2)
        self.assertEqual(function_default_param(5), 5)
        self.obj['f1'] = self.dumps(function_default_param)

    def test_function_multi_param_with_default(self):
        self.assertEqual(function_two_param_with_default_param(5), 7)
        self.assertEqual(function_two_param_with_default_param(5,10), 15)
        self.obj['f1'] = self.dumps(function_two_param_with_default_param)

    def test_function_with_inner_import(self):
        self.assertEqual(function_inner_import([3,6,-1,9,3]), 3)
        self.obj['f1'] = self.dumps(function_inner_import)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()