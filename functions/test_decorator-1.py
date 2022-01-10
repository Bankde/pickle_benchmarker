#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Decorators
- Simple decorator
- Function with decorator
- Function with multiple decorators
- Function with decorator with arguments
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

def quote_decorator(function):
    def wrapper(arg1, arg2):
        arg1 = arg1.capitalize()
        arg2 = "\"" + arg2 + "\""
        return function(arg1, arg2)
    return wrapper

@quote_decorator
def sayWithQuote(name, sentence):
    return "{0} says {1}".format(name, sentence)

def capitalize_decorator(function):
    def wrapper(*args):
        result = function(*args)
        return result.upper()
    return wrapper

@capitalize_decorator
@quote_decorator
def sayWithQuoteAndCap(name, sentence):
    return "{0} says {1}".format(name, sentence)

def repeat_decorator(N):
    def decorator(func):
        def wrapper(*args):
            result = []
            for i in range(N):
                result.append(func(*args))
            return "\n".join(result)
        return wrapper
    return decorator

@repeat_decorator(3)
@quote_decorator
def sayWithQuoteRepeat(name, sentence):
    return "{0} says {1}".format(name, sentence)

class Test(helper.PickleTest):
    def test_decorator(self):
        self.assertEqual(sayWithQuote("john","hello world"), "John says \"hello world\"")
        self.obj['d1'] = self.dumps(quote_decorator)

    def test_function_with_decorator(self):
        self.assertEqual(sayWithQuote("john","hello world"), "John says \"hello world\"")
        self.obj['f1'] = self.dumps(sayWithQuote)

    def test_function_with_multiple_decorator(self):
        self.assertEqual(sayWithQuoteAndCap("john","hello world"), "JOHN SAYS \"HELLO WORLD\"")
        self.obj['f1'] = self.dumps(sayWithQuoteAndCap)

    def test_function_with_decorator_with_argument(self):
        self.assertEqual(sayWithQuoteRepeat("john","hello world"), "John says \"hello world\"\nJohn says \"hello world\"\nJohn says \"hello world\"")
        self.obj['f1'] = self.dumps(sayWithQuoteRepeat)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()