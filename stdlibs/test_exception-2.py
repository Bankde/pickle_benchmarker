#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

class Test(helper.PickleTest):
    def test_builtin_exception(self):
        exc = self.loads(self.obj['exc'])
        self.assertEqual(repr(exc), "RuntimeError('testErr')")

    def test_user_exception(self):
        exc = self.loads(self.obj['exc'])
        self.assertEqual(repr(exc), "CustomError('testErr')")

    def test_chained_exception(self):
        exc2 = self.loads(self.obj['exc'])
        self.assertEqual(repr(exc2), "RuntimeError('Double failed')")
        self.assertEqual(repr(exc2.__context__), "RuntimeError('testErr')")

    def test_exception_traceback(self):
        exc = self.loads(self.obj['exc'])
        self.assertEqual(repr(exc), "RuntimeError('testErr')")
        self.assertEqual(exc.__traceback__.tb_lineno, 55)
        self.assertEqual(exc.__traceback__.tb_next.tb_lineno, 22)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()