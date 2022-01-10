#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Functor
- Functor object (callable object)
- Functor class [Skip, no difference from regular class]
###### End of Description ######
'''

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

class Multiplier():
    def __init__(self, init):
        self.init = init

    def __call__(self, x):
        return x * self.init

class Test(helper.PickleTest):
    def test_functor_object_with_class_ref(self):
        ad = Adder(13)
        self.assertEqual(ad(19), 32)
        self.obj['ad'] = self.dumps(ad)

    def test_functor_object_without_class_ref(self):
        mul = Multiplier(13)
        self.assertEqual(mul(19), 247)
        self.obj['mul'] = self.dumps(mul)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()