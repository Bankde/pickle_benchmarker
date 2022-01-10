#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

sys.path.append(os.path.join(sys.path[0], "./dependencies"))
import test_3_mod_1
from datetime import timedelta
from base64 import b64encode
import types
class Test(helper.PickleTest):
    def test_custom_function(self):
        self.assertEqual(self.loads(self.obj['f1'])(5,7), 35)
        
    def test_custom_class(self):
        self.assertEqual(str(self.loads(self.obj['c1'])("world")), "hello world")
        self.assertEqual(str(self.loads(self.obj['o1'])), "hello world")

    def test_module(self):
        test_3_mod_2 = self.loads(self.obj['m1'])
        self.assertIsInstance(test_3_mod_2, types.ModuleType)
        self.assertEqual(str(test_3_mod_2.CustomClass(9)), "81")

    def test_python_lib(self):
        self.assertEqual(self.loads(self.obj['f1'])(b'test'), b'dGVzdA==')
        self.assertEqual(self.loads(self.obj['c1'])(days=50).days, 50)
        self.assertEqual(self.loads(self.obj['o1']).days, 50)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()