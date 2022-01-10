#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Function/class from other modules
- Function from user's module
- Class from user's module
- Obj from Class from user's module
- User's module
- Function from standard python module
- Class from standard python module
- Obj from Class from standard python module
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], "../utilities"))
import helper

########## Code Here ##########

sys.path.append(os.path.join(sys.path[0], "./dependencies"))
import test_3_mod_1
from datetime import timedelta
from base64 import b64encode
import types
class Test(helper.PickleTest):
    def test_custom_function(self):
        self.assertEqual(test_3_mod_1.customFunction(5,7), 35)
        self.obj['f1'] = self.dumps(test_3_mod_1.customFunction)
        
    def test_custom_class(self):
        self.assertEqual(str(test_3_mod_1.CustomClass("world")), "hello world")
        self.obj['c1'] = self.dumps(test_3_mod_1.CustomClass)
        self.obj['o1'] = self.dumps(test_3_mod_1.CustomClass("world"))

    def test_module(self):
        import test_3_mod_2
        self.obj['m1'] = self.dumps(test_3_mod_2)
        self.assertIsInstance(test_3_mod_2, types.ModuleType)
        self.assertEqual(str(test_3_mod_2.CustomClass(9)), "81")

    def test_python_lib(self):
        self.assertEqual(b64encode(b'test'), b'dGVzdA==')
        self.assertEqual(timedelta(days=50).days, 50)
        self.obj['f1'] = self.dumps(b64encode)
        self.obj['c1'] = self.dumps(timedelta)
        self.obj['o1'] = self.dumps(timedelta(days=50))

    def test_custom_function_without_import(self):
        self.assertEqual(test_3_mod_1.customFunction(5,7), 35)
        self.obj['f1'] = self.dumps(test_3_mod_1.customFunction)
        
    def test_custom_class_without_import(self):
        self.assertEqual(str(test_3_mod_1.CustomClass("world")), "hello world")
        self.obj['c1'] = self.dumps(test_3_mod_1.CustomClass)
        self.obj['o1'] = self.dumps(test_3_mod_1.CustomClass("world"))

    def test_python_lib_without_import(self):
        self.assertEqual(b64encode(b'test'), b'dGVzdA==')
        self.assertEqual(timedelta(days=50).days, 50)
        self.obj['f1'] = self.dumps(b64encode)
        self.obj['c1'] = self.dumps(timedelta)
        self.obj['o1'] = self.dumps(timedelta(days=50))

    def test_custom_function_without_import_and_path(self):
        self.assertEqual(test_3_mod_1.customFunction(5,7), 35)
        self.obj['f1'] = self.dumps(test_3_mod_1.customFunction)
        
    def test_custom_class_without_import_and_path(self):
        self.assertEqual(str(test_3_mod_1.CustomClass("world")), "hello world")
        self.obj['c1'] = self.dumps(test_3_mod_1.CustomClass)
        self.obj['o1'] = self.dumps(test_3_mod_1.CustomClass("world"))

    def test_module_without_path(self):
        import test_3_mod_2
        self.obj['m1'] = self.dumps(test_3_mod_2)
        self.assertIsInstance(test_3_mod_2, types.ModuleType)
        self.assertEqual(str(test_3_mod_2.CustomClass(9)), "81")

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()