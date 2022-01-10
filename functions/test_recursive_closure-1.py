#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Recursive Closure
- Direct recursive closure
- Indirect recursive closure
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

def closure_direct_recursive():
    def divideTwo(x):
        if x <= 10: return x
        return divideTwo(x//2)
    return divideTwo

def closure_indirect_recursive():
    def divideTwo(x):
        if x <= 10: return x
        return divideThree(x//2)
    def divideThree(x):
        if x <= 10: return x
        return divideTwo(x//3)
    return divideTwo

class Test(helper.PickleTest):
    def test_closure_direct_recursive(self):
        self.assertEqual(closure_direct_recursive()(150), 9)
        self.obj['c1'] = self.dumps(closure_direct_recursive())
        self.obj['f1'] = self.dumps(closure_direct_recursive)

    def test_closure_indirect_recursive(self):
        self.assertEqual(closure_indirect_recursive()(150), 4)
        self.obj['c1'] = self.dumps(closure_indirect_recursive())
        self.obj['f1'] = self.dumps(closure_indirect_recursive)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()