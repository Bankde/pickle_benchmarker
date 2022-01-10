#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import asyncio

class Test(helper.PickleTest):
    def test_coroutine_function(self):
        f = self.loads(self.obj['f'])
        self.assertEqual(asyncio.run(f(13)), 39)

    def test_coroutine_object(self):
        o = self.loads(self.obj['o'])
        self.assertEqual(asyncio.run(o), 39)

    def test_func_with_await(self):
        f = self.loads(self.obj['f'])
        self.assertEqual(asyncio.run(f(4)), 144)

    def test_task(self):
        loop = asyncio.new_event_loop()
        try:
            task = self.loads(self.obj['t'])
            loop.run_until_complete(task)
            self.assertEqual(task.result(), 39)
        finally:
            loop.close()

    def test_asyncio_future(self):
        loop = asyncio.new_event_loop()
        try:
            future = self.loads(self.obj['f'])
            self.assertEqual(future.done(), False)
            self.assertEqual(future.cancelled(), False)
            future.set_result("I'm done")
            self.assertEqual(future.done(), True)
            self.assertEqual(future.result(), "I'm done")
        finally:
            loop.close()

    def test_event_loop(self):
        async def tmp_coroutine_func(x):
            return x*3
        loop = self.loads(self.obj['l'])
        task = loop.create_task(tmp_coroutine_func(13))
        loop.run_until_complete(task)
        self.assertEqual(task.result(), 39)
        loop.close()
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()