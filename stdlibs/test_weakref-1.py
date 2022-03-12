#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Weakref
- Weakref to Python standard object
- Weakref to custom class's object
- Weakref proxy
- Weakref callable proxy
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import weakref

class CustomObject():
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return self.val

class Test(helper.PickleTest):
    def test_weakref_to_set(self):
        o = set([1,2,3,4,5])
        r = weakref.ref(o)
        self.obj['o'] = self.dumps(o)
        self.obj['r'] = self.dumps(r)
        o2 = r()
        self.assertEqual(o2, set([1,2,3,4,5]))
        with self.memTest():
            self.assertTrue(o is o2)
            self.assertEqual(weakref.getweakrefcount(o), 1)

    def test_weakref_to_custom_object(self):
        o = CustomObject(13)
        r = weakref.ref(o)
        self.obj['o'] = self.dumps(o)
        self.obj['r'] = self.dumps(r)
        o2 = r()
        self.assertEqual(o2.__class__.__name__, "CustomObject")
        self.assertEqual(o2.val, 13)
        with self.memTest():
            self.assertTrue(o is o2)
            self.assertEqual(weakref.getweakrefcount(o), 1)

    def test_bundled_weakref(self):
        o = set([1,2,3,4,5])
        r = weakref.ref(o)
        bundle = {'o': o, 'r': r}
        self.obj['b'] = self.dumps(bundle)
        o2 = bundle['r']()
        self.assertEqual(o2, set([1,2,3,4,5]))
        with self.memTest():
            self.assertTrue(bundle['o'] is o2)
            self.assertEqual(weakref.getweakrefcount(bundle['o']), 1)

    def test_weakref_proxy(self):
        o = set([1,2,3,4,5])
        p = weakref.proxy(o)
        self.obj['o'] = self.dumps(o)
        self.obj['p'] = self.dumps(p)
        self.assertEqual(str(p), '{1, 2, 3, 4, 5}')
        with self.memTest():
            self.assertIsInstance(p, weakref.ProxyType)
            self.assertEqual(weakref.getweakrefcount(o), 1)

    def test_weakref_callable_proxy(self):
        def func(a):
            return a*3
        f = func
        p = weakref.proxy(f)
        self.obj['f'] = self.dumps(f)
        self.obj['p'] = self.dumps(p)
        self.assertEqual(p(13), 39)
        with self.memTest():
            self.assertIsInstance(p, weakref.CallableProxyType)
            self.assertEqual(weakref.getweakrefcount(f), 1)

    def test_bundled_weakref_proxy(self):
        o = set([1,2,3,4,5])
        p = weakref.proxy(o)
        bundle = {'o': o, 'p': p}
        self.obj['b'] = self.dumps(bundle)
        self.assertEqual(str(bundle['p']), '{1, 2, 3, 4, 5}')
        with self.memTest():
            self.assertIsInstance(bundle['p'], weakref.ProxyType)
            self.assertEqual(weakref.getweakrefcount(bundle['o']), 1)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()