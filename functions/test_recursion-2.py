#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

class Test(helper.PickleTest):
    def test_direct_recursion(self):
        self.assertEqual(self.loads(self.obj['f1'])(17), 36)

    def test_direct_recursion_multi(self):
        self.assertEqual(self.loads(self.obj['f1'])(17), 58)

    def test_direct_nested_recursion(self):
        self.assertEqual(self.loads(self.obj['f1'])(17), 36)

    def test_indirect_recursion(self):
        self.assertEqual(self.loads(self.obj['f1'])(17), 37)
        self.assertEqual(self.loads(self.obj['f2'])(17), 30)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()