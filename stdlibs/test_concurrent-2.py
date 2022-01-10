#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import concurrent.futures

class Test(helper.PickleTest):
    def test_concurrent_future_object(self):
        future = self.loads(self.obj['future'])
        self.fail("Unable to acquire lock object inside the future")
        # # Underlying object has lock that blocks forever.
        # self.assertEqual(future.result(), 81)

    def test_thread_pool_executor(self):
        executor = self.loads(self.obj['exec'])
        a = executor.submit(pow, 3, 4)
        b = executor.submit(pow, 5, 6)
        self.assertEqual(a.result(), 81)
        self.assertEqual(b.result(), 15625)

    def test_process_pool_executor(self):
        executor = self.loads(self.obj['exec'])
        a = executor.submit(pow, 3, 4)
        b = executor.submit(pow, 5, 6)
        self.assertEqual(a.result(), 81)
        self.assertEqual(b.result(), 15625)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()