#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Coroutine
- Coroutine function
- Coroutine object
- Task object
- Asyncio-future object
- Event loop
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import asyncio

async def coroutine_func(x):
    return x*3

async def nested(y):
    return y**2

async def coroutine_nested_func(x):
    return await nested(x*3)

class Test(helper.PickleTest):
    def test_coroutine_function(self):
        f = coroutine_func
        self.obj['f'] = self.dumps(f)
        self.assertEqual(asyncio.run(f(13)), 39)

    def test_coroutine_object(self):
        o = coroutine_func(13)
        try:
            self.obj['o'] = self.dumps(o)
        finally:
            self.assertEqual(asyncio.run(o), 39)

    def test_func_with_await(self):
        f = coroutine_nested_func
        self.obj['f'] = self.dumps(f)
        self.assertEqual(asyncio.run(f(4)), 144)

    def test_task(self):
        loop = asyncio.new_event_loop()
        task = loop.create_task(coroutine_func(13))
        try:
            self.obj['t'] = self.dumps(task)
        finally:
            loop.run_until_complete(task)
            self.assertEqual(task.result(), 39)
            loop.close()

    def test_asyncio_future(self):
        loop = asyncio.new_event_loop()
        future = loop.create_future()
        try:
            self.obj['f'] = self.dumps(future)
        finally:
            self.assertEqual(future.done(), False)
            self.assertEqual(future.cancelled(), False)
            future.set_result("I'm done")
            self.assertEqual(future.done(), True)
            self.assertEqual(future.result(), "I'm done")
            loop.close()

    def test_event_loop(self):
        async def tmp_coroutine_func(x):
            return x*3
        loop = asyncio.new_event_loop()
        self.obj['l'] = self.dumps(loop)
        task = loop.create_task(tmp_coroutine_func(13))
        loop.run_until_complete(task)
        self.assertEqual(task.result(), 39)
        loop.close()
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()