#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import types
class Test(helper.PickleTest):
    def test_custom_function_without_import_and_path(self):
        self.assertEqual(self.loads(self.obj['f1'])(5,7), 35)
        
    def test_custom_class_without_import_and_path(self):
        self.assertEqual(str(self.loads(self.obj['c1'])("world")), "hello world")
        self.assertEqual(str(self.loads(self.obj['o1'])), "hello world")

    def test_module_without_path(self):
        test_3_mod_2 = self.loads(self.obj['m1'])
        self.assertIsInstance(test_3_mod_2, types.ModuleType)
        o = test_3_mod_2.CustomClass(9)
        self.assertEqual(str(o), "81")
        o.add(2)
        self.assertEqual(str(o), "83")

    @unittest.skipIf(helper.pickle.__name__ != "cloudpickle", "Only test for cloudpickle")
    def test_custom_function_without_import_and_path_forced_value(self):
        self.assertEqual(self.loads(self.obj['f1'])(5,7), 35)

    @unittest.skipIf(helper.pickle.__name__ != "cloudpickle", "Only test for cloudpickle")
    def test_custom_class_without_import_and_path_forced_value(self):
        self.assertEqual(str(self.loads(self.obj['c1'])("world")), "hello world")
        self.assertEqual(str(self.loads(self.obj['o1'])), "hello world")

    @unittest.skipIf(helper.pickle.__name__ != "cloudpickle", "Only test for cloudpickle")
    def test_module_without_path_forced_value(self):
        test_3_mod_2 = self.loads(self.obj['m1'])
        self.assertIsInstance(test_3_mod_2, types.ModuleType)
        o = test_3_mod_2.CustomClass(9)
        self.assertEqual(str(o), "81")
        o.add(2)
        self.assertEqual(str(o), "83")
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()