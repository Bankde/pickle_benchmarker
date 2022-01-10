#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import weakref

class Test(helper.PickleTest):
    def test_weakref_to_set(self):
        o = self.loads(self.obj['o'])
        r = self.loads(self.obj['r'])
        o2 = r()
        self.assertEqual(o2, set([1,2,3,4,5]))
        with self.memTest():
            self.assertTrue(o is o2)
            self.assertEqual(weakref.getweakrefcount(o), 1)

    def test_weakref_to_custom_object(self):
        o = self.loads(self.obj['o'])
        r = self.loads(self.obj['r'])
        o2 = r()
        self.assertEqual(o2.__class__.__name__, "CustomObject")
        self.assertEqual(o2.val, 13)
        with self.memTest():
            self.assertTrue(o is o2)
            self.assertEqual(weakref.getweakrefcount(o), 1)

    def test_weakref_proxy(self):
        o = self.loads(self.obj['o'])
        p = self.loads(self.obj['p'])
        self.assertEqual(str(p), '{1, 2, 3, 4, 5}')
        with self.memTest():
            self.assertIsInstance(p, weakref.ProxyType)
            self.assertEqual(weakref.getweakrefcount(o), 1)

    def test_weakref_callable_proxy(self):
        f = self.loads(self.obj['f'])
        p = self.loads(self.obj['p'])
        self.assertEqual(p(13), 39)
        with self.memTest():
            self.assertIsInstance(p, weakref.CallableProxyType)
            self.assertEqual(weakref.getweakrefcount(f), 1)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()