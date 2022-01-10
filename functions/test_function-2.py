#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########
class Test(helper.PickleTest):
    def test_function_param(self):
        self.assertEqual(self.loads(self.obj['f1'])(5), 5)
        self.assertEqual(self.loads(self.obj['f2'])(5,7), 12)

    def test_function_default_param(self):
        self.assertEqual(self.loads(self.obj['f1'])(), 2)
        self.assertEqual(self.loads(self.obj['f1'])(5), 5)

    def test_function_multi_param_with_default(self):
        self.assertEqual(self.loads(self.obj['f1'])(5), 7)
        self.assertEqual(self.loads(self.obj['f1'])(5,10), 15)

    def test_function_with_inner_import(self):
        self.assertEqual(self.loads(self.obj['f1'])([3,6,-1,9,3]), 3)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()
