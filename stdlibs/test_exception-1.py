#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Exception
- Builtin exception
- User-defined exception
- Chained exception
- Exception with traceback check
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

def funcError(err):
    raise err

class CustomError(Exception):
    pass

class Test(helper.PickleTest):
    def test_builtin_exception(self):
        try:
            funcError(RuntimeError("testErr"))
        except Exception as exc:
            self.assertEqual(repr(exc), "RuntimeError('testErr')")
            self.obj['exc'] = self.dumps(exc)

    def test_user_exception(self):
        try:
            funcError(CustomError("testErr"))
        except Exception as exc:
            self.assertEqual(repr(exc), "CustomError('testErr')")
            self.obj['exc'] = self.dumps(exc)

    def test_chained_exception(self):
        try:
            try:
                funcError(RuntimeError("testErr"))
            except Exception as exc1:
                raise RuntimeError('Double failed') from exc1
        except Exception as exc2:
            self.assertEqual(repr(exc2), "RuntimeError('Double failed')")
            self.assertEqual(repr(exc2.__context__), "RuntimeError('testErr')")
            self.obj['exc'] = self.dumps(exc2)

    def test_exception_traceback(self):
        try:
            funcError(RuntimeError("testErr"))
        except Exception as exc:
            self.assertEqual(repr(exc), "RuntimeError('testErr')")
            self.assertEqual(exc.__traceback__.tb_lineno, 55)
            self.assertEqual(exc.__traceback__.tb_next.tb_lineno, 22)
            self.obj['exc'] = self.dumps(exc)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()