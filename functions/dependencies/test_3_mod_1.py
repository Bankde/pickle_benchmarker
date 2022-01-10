#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CustomClass():
    def __init__(self, s):
        self.a = "hello"
        self.b = s

    def __str__(self):
        return self.a + " " + self.b

def customFunction(a, b):
    return a*b