#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import operator

class Student():
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
        self.grade = "A" if score > 90 else "F"

class Test(helper.PickleTest):
    def test_attrgetter(self):
        std1 = Student("Sam", 15, 80)
        f = self.loads(self.obj['f'])
        self.assertEqual(f(std1), ("Sam", "F"))

    def test_itemgetter(self):
        arr1 = [1,2,3,4,5,6,7,8,9,10]
        str1 = "ABCDEFGHIJKLMNOP"
        f = self.loads(self.obj['f'])
        self.assertEqual(f(arr1), (4,2,6))
        self.assertEqual(f(str1), ("D","B","F"))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()