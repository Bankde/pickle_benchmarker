#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CustomClass():
    def __init__(self, val):
        self.val = val**2

    def add(self, n):
        self.val += n

    def __str__(self):
        return str(self.val)