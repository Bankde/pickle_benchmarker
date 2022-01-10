#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Closure
- Simple closure (read/write)
- Mutated closure
- Function that return closure (read/write)
- Closure with nonlocal
- Multiple level closure and function
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from functools import reduce

def closure_simple_read(a):
    init = a
    def add(x):
        return init+x
    return add

def closure_simple_write(a):
    init = [a]
    def addAndSum(x):
        init.append(x)
        return sum(init)
    return addAndSum

def closure_counter(a):
    init = a
    def count(x):
        nonlocal init
        init += x
        return init
    return count

def closure_multi_level_1(a,b):
    lv1 = a
    def closure_multi_level_2(x):
        lv2 = b + x
        def closure_multi_level_3(y):
            return (y + lv1)**2 + (y + lv2)
        return closure_multi_level_3
    return closure_multi_level_2

class Test(helper.PickleTest):
    def test_simple_closure(self):
        self.assertEqual(closure_simple_read(17)(18), 35)
        self.obj['c1'] = self.dumps(closure_simple_read(17))
        add_and_sum = closure_simple_write(3)
        self.assertEqual(add_and_sum(5), 8)
        self.assertEqual(add_and_sum(17), 25)
        self.obj['c2'] = self.dumps(closure_simple_write(3))

    def test_mutated_closure(self):
        add_and_sum = closure_simple_write(3)
        self.assertEqual(add_and_sum(5), 8)
        self.assertEqual(add_and_sum(17), 25)
        self.obj['c1'] = self.dumps(add_and_sum)

    def test_function_return_closure(self):
        self.assertEqual(closure_simple_read(17)(18), 35)
        self.obj['f1'] = self.dumps(closure_simple_read)
        add_and_sum = closure_simple_write(3)
        self.assertEqual(add_and_sum(5), 8)
        self.assertEqual(add_and_sum(17), 25)
        self.obj['f2'] = self.dumps(closure_simple_write)

    def test_closure_non_local(self):
        counter = closure_counter(10)
        self.assertEqual(counter(5), 15)
        self.assertEqual(counter(7), 22)
        self.obj['c1'] = self.dumps(closure_counter(10))

    def test_closure_multi_level(self):
        # (6 + 3)**2 + (6 + (4 + 5))
        self.assertEqual(closure_multi_level_1(3,4)(5)(6), 96)
        self.obj['f1'] = self.dumps(closure_multi_level_1)
        self.obj['c1'] = self.dumps(closure_multi_level_1(3,4))
        c = closure_multi_level_1(3,4)(5)
        self.assertEqual(c(6), 96)
        self.assertEqual(c(7), 116)
        self.obj['c2'] = self.dumps(closure_multi_level_1(3,4)(5))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()