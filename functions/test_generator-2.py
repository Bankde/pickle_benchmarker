#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

class Test(helper.PickleTest):
    def test_generator_expression(self):
        self.assertEqual(list(self.loads(self.obj['g1'])), [0,1,2,3,4,5,6,7,8,9])
        self.assertEqual(list(self.loads(self.obj['g2'])), [0,1,4,9,16,25,36,49,64,81])

    def test_generator_function(self):
        g = self.loads(self.obj['f1'])(10)
        self.assertEqual(next(g), 10)
        self.assertEqual(next(g), 20)
        self.assertEqual(next(g), 40)

    def test_function_yield_get_val(self):
        g = self.loads(self.obj['f1'])(10)
        self.assertEqual(g.send(None), 10)
        self.assertEqual(g.send(3), 23)
        self.assertEqual(g.send(13), 59)

    def test_generator_object(self):
        g1 = self.loads(self.obj['g1'])
        self.assertEqual(next(g1), 80)
        self.assertEqual(next(g1), 160)
        self.assertEqual(next(g1), 320)
        g2 = self.loads(self.obj['g2'])
        self.assertEqual(next(g2), 10)
        self.assertEqual(next(g2), 20)
        self.assertEqual(next(g2), 40)

    def test_function_yield_from(self):
        def tmp_function_yield(x):
            cur = x
            while True:
                adder = yield cur
                cur = cur*2 + adder
        g = tmp_function_yield(10)
        w = self.loads(self.obj['f1'])(g)
        self.assertEqual(w.send(None), 10)
        self.assertEqual(w.send(3), 23)
        self.assertEqual(w.send(13), 59)

    def test_generator_frame_object(self):
        frame = self.loads(self.obj['f1'])
        self.assertEqual(frame.f_lineno, 28)
        self.assertEqual(frame.f_lasti, 8)
        self.assertDictEqual(frame.f_locals, {'x':10, 'cur':10})

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()