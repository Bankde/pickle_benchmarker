#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

class Test(helper.PickleTest):
    def test_decorator(self):
        quote_decorator = self.loads(self.obj['d1'])
        @quote_decorator
        def sayWithQuote(name, sentence):
            return "{0} says {1}".format(name, sentence)
        self.assertEqual(sayWithQuote("john","hello world"), "John says \"hello world\"")

    def test_function_with_decorator(self):
        sayWithQuote = self.loads(self.obj['f1'])
        self.assertEqual(sayWithQuote("john","hello world"), "John says \"hello world\"")

    def test_function_with_multiple_decorator(self):
        sayWithQuoteAndCap = self.loads(self.obj['f1'])
        self.assertEqual(sayWithQuoteAndCap("john","hello world"), "JOHN SAYS \"HELLO WORLD\"")

    def test_function_with_decorator_with_argument(self):
        sayWithQuoteRepeat = self.loads(self.obj['f1'])
        self.assertEqual(sayWithQuoteRepeat("john","hello world"), "John says \"hello world\"\nJohn says \"hello world\"\nJohn says \"hello world\"")

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()