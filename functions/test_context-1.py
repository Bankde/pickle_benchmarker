#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Context
- Function with context "with" expression
- Context manager object
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from decimal import Decimal, localcontext
import io

def function_with_context(num, prec):
    with localcontext() as ctx:
        ctx.prec = prec
        return Decimal("1") / Decimal(str(num))

contextManager1 = localcontext()

class UserContextManager(object):
    def __init__(self, logger):
        self.logger = logger

    def __enter__(self):
        self.logger.write("Enter context\n")
        return self.logger

    def __exit__(self, type, value, traceback):
        self.logger.write("Exit context\n")

class Test(helper.PickleTest):
    def test_function_with_context(self):
        self.assertEqual(function_with_context(41, 50), Decimal("0.024390243902439024390243902439024390243902439024390"))
        self.obj['f1'] = self.dumps(function_with_context)

    def test_context_manager(self):
        with contextManager1 as ctx:
            ctx.prec = 50
            result = Decimal("1") / Decimal("41")
        self.assertEqual(result, Decimal("0.024390243902439024390243902439024390243902439024390"))
        self.obj['c1'] = self.dumps(contextManager1)

    def test_user_context_manager(self):
        logger = io.StringIO()
        with UserContextManager(logger) as log:
            self.assertEqual(logger.getvalue(), "Enter context\n")
            log.write("Hello\n")
            self.assertEqual(logger.getvalue(), "Enter context\nHello\n")
        self.assertEqual(logger.getvalue(), "Enter context\nHello\nExit context\n")
        self.obj['c1'] = self.dumps(UserContextManager)

        logger2 = io.StringIO()
        self.obj['c2'] = self.dumps(UserContextManager(logger2))

    def test_context(self):
        with contextManager1 as ctx:
            ctx.prec = 50
            result = Decimal("1") / Decimal("41")
            self.assertEqual(result, Decimal("0.024390243902439024390243902439024390243902439024390"))
            self.obj['c1'] = self.dumps(ctx)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()