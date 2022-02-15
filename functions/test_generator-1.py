#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Generator
- Standard generator expression
- Generator function (Yield)
- Function with yield that get values back from send
- Generator object
- Function with yield from
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

gen1 = range(10)
gen2 = (x**2 for x in range(10))

def function_generator(x):
    cur = x
    while True:
        yield cur
        cur = cur*2

def function_get_val_from_yield(x):
    cur = x
    while True:
        adder = yield cur
        cur = cur*2 + adder

def function_yield_from(coro):
    yield from coro

class Test(helper.PickleTest):
    def test_generator_expression(self):
        self.assertEqual(list(gen1), [0,1,2,3,4,5,6,7,8,9])
        self.assertEqual(list(gen2), [0,1,4,9,16,25,36,49,64,81])
        self.obj['g1'] = self.dumps(gen1)
        self.obj['g2'] = self.dumps(gen2)

    def test_generator_function(self):
        g = function_generator(10)
        self.assertEqual(next(g), 10)
        self.assertEqual(next(g), 20)
        self.assertEqual(next(g), 40)
        self.obj['f1'] = self.dumps(function_generator)

    def test_function_yield_get_val(self):
        g = function_get_val_from_yield(10)
        self.assertEqual(g.send(None), 10)
        self.assertEqual(g.send(3), 23)
        self.assertEqual(g.send(13), 59)
        self.obj['f1'] = self.dumps(function_get_val_from_yield)

    def test_generator_object(self):
        g1 = function_generator(10)
        self.assertEqual(next(g1), 10)
        self.assertEqual(next(g1), 20)
        self.assertEqual(next(g1), 40)
        self.obj['g1'] = self.dumps(g1)
        g2 = function_generator(10)
        self.obj['g2'] = self.dumps(g2)

    def test_function_yield_from(self):
        def tmp_function_yield(x):
            cur = x
            while True:
                adder = yield cur
                cur = cur*2 + adder
        g = tmp_function_yield(10)
        w = function_yield_from(g)
        self.assertEqual(w.send(None), 10)
        self.assertEqual(w.send(3), 23)
        self.assertEqual(w.send(13), 59)
        self.obj['f1'] = self.dumps(function_yield_from)

    def test_generator_frame_object(self):
        g1 = function_generator(10)
        self.assertEqual(next(g1), 10)
        frame = g1.gi_frame
        self.assertEqual(frame.f_lineno, 28)
        self.assertEqual(frame.f_lasti, 8)
        self.assertDictEqual(frame.f_locals, {'x':10, 'cur':10})
        self.obj['f1'] = self.dumps(frame)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()