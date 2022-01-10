#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Classes
- Simple class
- Class with inheritances
- Class with property object
- Object from user class (main) without reference
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

class ClassOne():
    '''
    Simple class
    '''
    def __init__(self, a):
        self.a = a
    def func_one(self, a):
        return self.a + a
class ClassTwo(int):
    '''
    Simple class inheritance
    '''
    def __new__(cls, value, *args, **kwargs):
        return super(ClassTwo, cls).__new__(cls, value)
    def __str__(self):
        return "Even: %d" % (int(self)*2)
class ClassThree(int):
    '''
    Similar to ClassTwo: bad practice but support by Dill
    '''
    def __new__(cls, value, *args, **kwargs):
        return int.__new__(cls, value)
    def __str__(self):
        return "Even: %d" % (int(self)*2)
class ClassFour(int):
    '''
    Example that pickler does not copy memory but instead recursively reads their attributes and frame them.
    pickle.loads(pickle.dumps(ClassFour(7))) = 14
    This is because pickle reads the object's attribute during pickle.dumps and it returns 14 (Not 7).
    New the object again during pickle.loads causes it to call init again and thus returns 28.
    '''
    def __new__(cls, value, *args, **kwargs):
        return int.__new__(cls, value*2)
    def __str__(self):
        return "Even: %d" % int(self)

class ClassFive():
    '''
    Class with property object.
    '''
    def __init__(self):
        self._x = None
    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, "I'm the property object")

class ClassSix():
    def __init__(self, x):
        self.x = x

    def getVal(self):
        return "Hello " + self.x

class Test(helper.PickleTest):
    def test_simple_class(self):
        self.assertEqual(ClassOne(10).func_one(5), 15)
        self.obj['c1'] = self.dumps(ClassOne)
        o = ClassOne(11)
        self.assertEqual(o.func_one(13), 24)
        self.assertEqual(o.__class__.__name__, "ClassOne")
        self.obj['o1'] = self.dumps(o)
        
    def test_class_super_var_1(self):
        self.assertEqual(str(ClassTwo(7)), "Even: 14")
        self.obj['c1'] = self.dumps(ClassTwo)
        self.obj['o1'] = self.dumps(ClassTwo(7))

    def test_class_super_var_2(self):
        self.assertEqual(str(ClassThree(7)), "Even: 14")
        self.obj['c1'] = self.dumps(ClassThree)
        self.obj['o1'] = self.dumps(ClassThree(7))

    def test_class_reinit_attr(self):
        self.assertEqual(str(ClassFour(7)), "Even: 14")
        self.obj['o1'] = self.dumps(ClassFour(7))

    def test_class_with_property_object(self):
        o = ClassFive()
        self.assertEqual(o.x, None)
        o.x = 1234
        self.assertEqual(o.x, 1234)
        del o.x
        self.assertFalse(hasattr(o, 'x'))
        self.obj['c1'] = self.dumps(ClassFive)

    def test_object_without_class_reference(self):
        o = ClassSix("world")
        self.assertEqual(o.x, "world")
        self.assertEqual(o.getVal(), "Hello world")
        self.assertEqual(o.__class__.__name__, "ClassSix")
        self.obj['o1'] = self.dumps(o)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()