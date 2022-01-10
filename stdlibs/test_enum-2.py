#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Enum
- Enum class
- Enum value with clas definition
- Enum value without class definition
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from enum import Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Test(helper.PickleTest):
    def test_enum_class_with_class_definition(self):
        color = self.loads(self.obj['class'])
        with self.memTest():
            self.assertIsInstance(color.GREEN, Color)
        self.assertEqual(color.RED.name, "RED")
        self.assertEqual(color.BLUE.value, 3)

    def test_enum_class_without_class_definition(self):
        shape = self.loads(self.obj['class'])
        self.assertEqual(shape.CIRCLE.__class__.__name__, "Shape")
        self.assertEqual(shape.TRIANGLE.name, "TRIANGLE")
        self.assertEqual(shape.SQUARE.value, 3)

    def test_enum_val_with_class_definition(self):
        green = self.loads(self.obj['green'])
        self.obj['green'] = self.dumps(green)
        with self.memTest():
            self.assertIsInstance(green, Color)
        self.assertEqual(green.name, "GREEN")
        self.assertEqual(green.value, 2)

    def test_enum_val_without_class_definition(self):
        square = self.loads(self.obj['square'])
        self.assertEqual(square.__class__.__name__, "Shape")
        self.assertEqual(square.name, "SQUARE")
        self.assertEqual(square.value, 3)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()