#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Recursive Function
- Direct recursion
- Indirect recursion
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

def direct_recursion(a):
    if a <= 0: return 1
    return direct_recursion(a//2) + 7
def direct_recursion_multi(a):
    if a <= 0: return 1
    return direct_recursion(a//2) + direct_recursion(a//3) + 7
def direct_nested_recursion(a):
    if a <= 0: return 1
    return direct_recursion(direct_recursion(a//2)//3) + 7
def indirect_recursion_A(a):
    if a <= 0: return 1
    return indirect_recursion_B(a//2) + 7
def indirect_recursion_B(a):
    if a <= 0: return 1
    return indirect_recursion_A(a//3) + 11

class Test(helper.PickleTest):
    def test_direct_recursion(self):
        self.assertEqual(direct_recursion(17), 36)
        self.obj['f1'] = self.dumps(direct_recursion)

    def test_direct_recursion_multi(self):
        self.assertEqual(direct_recursion_multi(17), 58)
        self.obj['f1'] = self.dumps(direct_recursion_multi)

    def test_direct_nested_recursion(self):
        self.assertEqual(direct_nested_recursion(17), 36)
        self.obj['f1'] = self.dumps(direct_nested_recursion)

    def test_indirect_recursion(self):
        self.assertEqual(indirect_recursion_A(17), 37)
        self.obj['f1'] = self.dumps(indirect_recursion_A)
        self.assertEqual(indirect_recursion_B(17), 30)
        self.obj['f2'] = self.dumps(indirect_recursion_B)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()