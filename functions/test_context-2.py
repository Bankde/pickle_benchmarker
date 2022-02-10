#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from decimal import Decimal
import io

class Test(helper.PickleTest):
    def test_function_with_context(self):
        function_with_context = self.loads(self.obj['f1'])
        self.assertEqual(function_with_context(41, 50), Decimal("0.024390243902439024390243902439024390243902439024390"))

    def test_context_manager(self):
        contextManager1 = self.loads(self.obj['c1'])
        with contextManager1 as ctx:
            ctx.prec = 50
            result = Decimal("1") / Decimal("41")
        self.assertEqual(result, Decimal("0.024390243902439024390243902439024390243902439024390"))

    def test_user_context_manager(self):
        logger = io.StringIO()
        UserContextManager = self.loads(self.obj['c1'])
        with UserContextManager(logger) as log:
            self.assertEqual(logger.getvalue(), "Enter context\n")
            log.write("Hello\n")
            self.assertEqual(logger.getvalue(), "Enter context\nHello\n")
        self.assertEqual(logger.getvalue(), "Enter context\nHello\nExit context\n")

        with self.loads(self.obj['c2']) as log:
            self.assertEqual(log.getvalue(), "Enter context\n")
            log.write("Hello\n")
            self.assertEqual(log.getvalue(), "Enter context\nHello\n")

    def test_context(self):
        # This doesn't look like a correct way to test context but we couldn't find the way to test it.
        # It's weird we can __reduce__ ctx object, we shouldn't be able to.
        ctx = self.loads(self.obj['c1'])
        result = Decimal("1") / Decimal("41")
        self.assertEqual(result, Decimal("0.024390243902439024390243902439024390243902439024390"))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()