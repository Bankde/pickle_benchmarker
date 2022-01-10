#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Concurrent
- Concurrent.futures object
- Executor
- ThreadPoolExecutor
- It is not possible to pickle.dumps the Executor and Future object so no need to test on private properties of executor
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import concurrent.futures

class Test(helper.PickleTest):
    def test_concurrent_future_object(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        future = executor.submit(pow, 3, 4)
        self.obj['future'] = self.dumps(future)
        self.assertEqual(future.result(), 81)

    def test_thread_pool_executor(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.obj['exec'] = self.dumps(executor)
        a = executor.submit(pow, 3, 4)
        b = executor.submit(pow, 5, 6)
        self.assertEqual(a.result(), 81)
        self.assertEqual(b.result(), 15625)

    def test_process_pool_executor(self):
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
        self.obj['exec'] = self.dumps(executor)
        a = executor.submit(pow, 3, 4)
        b = executor.submit(pow, 5, 6)
        self.assertEqual(a.result(), 81)
        self.assertEqual(b.result(), 15625)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()