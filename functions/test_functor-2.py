#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import operator

class Adder():
    def __init__(self, init):
        self.init = init

    def __call__(self, x):
        return x + self.init

class Test(helper.PickleTest):
    def test_functor_object_with_class_ref(self):
        ad = self.loads(self.obj['ad'])
        self.assertEqual(ad(19), 32)

    def test_functor_object_without_class_ref(self):
        mul = self.loads(self.obj['mul'])
        self.assertEqual(mul(19), 247)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()