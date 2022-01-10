#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from functools import reduce

class Test(helper.PickleTest):
    def test_lambda(self):
        self.assertEqual(list(filter(self.loads(self.obj['l1']), ["hello", "wOrlD", "HELLO"])), ["hello", "HELLO"])
        self.assertEqual(list(map(self.loads(self.obj['l2']), [1,2,3,5,7])), [1,4,9,25,49])
        self.assertEqual(reduce(self.loads(self.obj['l3']), [1,2,3,5,7], 1), 210)

    def test_function_return_lambda(self):
        self.assertEqual(self.loads(self.obj['f1'])(18)(3), 108)
        self.assertEqual(self.loads(self.obj['l1'])(3), 102)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()