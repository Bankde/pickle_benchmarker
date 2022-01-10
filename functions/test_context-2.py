#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from decimal import Decimal, localcontext

class Test(helper.PickleTest):
    def test_function_with_context(self):
        function_with_context = self.loads(self.obj['f1'])
        self.assertEqual(function_with_context(41, 30), Decimal("0.0243902439024390243902439024390"))

    def test_context_manager(self):
        contextManager1 = self.loads(self.obj['c1'])
        with contextManager1 as ctx:
            ctx.prec = 30
            result = Decimal("1") / Decimal("41")
        self.assertEqual(result, Decimal("0.0243902439024390243902439024390"))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()