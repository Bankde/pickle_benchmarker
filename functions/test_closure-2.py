#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from functools import reduce

class Test(helper.PickleTest):
    def test_simple_closure(self):
        self.assertEqual(self.loads(self.obj['c1'])(18), 35)
        add_and_sum = self.loads(self.obj['c2'])
        self.assertEqual(add_and_sum(5), 8)
        self.assertEqual(add_and_sum(17), 25)

    def test_mutated_closure(self):
        add_and_sum = self.loads(self.obj['c1'])
        # Continue from 25
        self.assertEqual(add_and_sum(9), 34)
        self.assertEqual(add_and_sum(11), 45)

    def test_function_return_closure(self):
        closure_simple_read = self.loads(self.obj['f1'])
        self.assertEqual(closure_simple_read(17)(18), 35)
        closure_simple_write = self.loads(self.obj['f2'])
        add_and_sum = closure_simple_write(3)
        self.assertEqual(add_and_sum(5), 8)
        self.assertEqual(add_and_sum(17), 25)

    def test_closure_non_local(self):
        counter = self.loads(self.obj['c1'])
        self.assertEqual(counter(5), 15)
        self.assertEqual(counter(7), 22)

    def test_closure_multi_level(self):
        # (6 + 3)**2 + (6 + (4 + 5))
        self.assertEqual(self.loads(self.obj['f1'])(3,4)(5)(6), 96)
        self.assertEqual(self.loads(self.obj['c1'])(5)(6), 96)
        c = self.loads(self.obj['c2'])
        self.assertEqual(c(6), 96)
        self.assertEqual(c(7), 116)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()