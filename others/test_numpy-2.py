#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import numpy as np

class Test(helper.PickleTest):
    def test_array(self):
        x1 = self.loads(self.obj['x1'])
        x2 = self.loads(self.obj['x2'])
        x3 = self.loads(self.obj['x3'])
        self.assertIsInstance(x1, np.ndarray)
        self.assertEqual(x1.dtype, np.int32)
        self.assertTrue(np.array_equal(x1, np.array([[1, 2, 3], [4, 5, 6], [7,8,9]], np.int32)))
        self.assertIsInstance(x2, np.ndarray)
        self.assertTrue(np.array_equal(x2, np.ones(shape=(3, 4, 5, 6))))
        self.assertIsInstance(x3, np.ndarray)
        self.assertEqual(x3.dtype, np.cfloat)
        self.assertTrue(np.allclose(x3, np.array([1+2j, 2+2j, 3+2j, 4+2j, 5+2j], np.cfloat)))

    def test_dtype_object(self):
        dtype = self.loads(self.obj['dt'])
        self.assertIsInstance(dtype, np.dtype)
        self.assertEqual(dtype["re"], np.dtype('int16'))
        self.assertEqual(dtype["im"], np.dtype('int32'))

    def test_array_on_custom_dtype(self):
        x = self.loads(self.obj['x'])
        self.assertIsInstance(x, np.ndarray)
        self.assertEqual(x.dtype["re"], np.dtype('int16'))
        self.assertEqual(x.dtype["im"], np.dtype('int32'))
        self.assertEqual(x[0]["re"], 13)
        self.assertEqual(x[1]["im"], 17)

    def test_datetime(self):
        dt = self.loads(self.obj['datetime'])
        self.assertIsInstance(dt, np.datetime64)
        self.assertEqual(dt, np.datetime64('2005-02-25'))

        td = self.loads(self.obj['timedelta'])
        self.assertIsInstance(td, np.timedelta64)
        self.assertEqual(np.datetime64('2009-01-01') + td, np.datetime64('2009-01-14'))

    def test_constant(self):
        inf = self.loads(self.obj['inf'])
        self.assertTrue(np.isinf(inf))

        nan = self.loads(self.obj['nan'])
        self.assertTrue(np.isnan(nan))

        pi = self.loads(self.obj['pi'])
        self.assertTrue(np.isclose(pi, np.pi))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()