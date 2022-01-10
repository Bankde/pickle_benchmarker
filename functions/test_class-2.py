#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########
class Test(helper.PickleTest):
    def test_simple_class(self):
        cls = self.loads(self.obj['c1'])
        self.assertEqual(cls(10).func_one(5), 15)
        o = self.loads(self.obj['o1'])
        self.assertEqual(o.func_one(13), 24)
        self.assertEqual(o.__class__.__name__, "ClassOne")

    def test_class_super_var_1(self):
        cls = self.loads(self.obj['c1'])
        self.assertEqual(str(cls(7)), "Even: 14")
        o = self.loads(self.obj['o1'])
        self.assertEqual(str(o), "Even: 14")

    def test_class_super_var_2(self):
        cls = self.loads(self.obj['c1'])
        self.assertEqual(str(cls(7)), "Even: 14")
        o = self.loads(self.obj['o1'])
        self.assertEqual(str(o), "Even: 14")

    def test_class_reinit_attr(self):
        self.assertEqual(str(self.loads(self.obj['o1'])), "Even: 28")

    def test_class_with_property_object(self):
        cls = self.loads(self.obj['c1'])
        o = cls()
        self.assertEqual(o.x, None)
        o.x = 1234
        self.assertEqual(o.x, 1234)
        del o.x
        self.assertFalse(hasattr(o, 'x'))

    def test_object_without_class_reference(self):
        o = self.loads(self.obj['o1'])
        self.assertEqual(o.x, "world")
        self.assertEqual(o.getVal(), "Hello world")
        self.assertEqual(o.__class__.__name__, "ClassSix")

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()