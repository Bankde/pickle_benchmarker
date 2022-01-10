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
def function_with_context(num, prec):
    with localcontext() as ctx:
        ctx.prec = prec
        return Decimal("1") / Decimal(str(num))

contextManager1 = localcontext()

class Test(helper.PickleTest):
    def test_function_with_context(self):
        self.assertEqual(function_with_context(41, 30), Decimal("0.0243902439024390243902439024390"))
        self.obj['f1'] = self.dumps(function_with_context)

    def test_context_manager(self):
        with contextManager1 as ctx:
            ctx.prec = 30
            result = Decimal("1") / Decimal("41")
        self.assertEqual(result, Decimal("0.0243902439024390243902439024390"))
        self.obj['c1'] = self.dumps(contextManager1)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()