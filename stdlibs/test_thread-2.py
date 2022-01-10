#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import threading
import concurrent.futures
import re
import time

result_file = os.path.join(sys.path[0], "./dependencies", "test_thread_result.tmp")
open(result_file, "w+").close() # Reset the file

def checkLastLine():
    with open(result_file, "r") as f:
        last_line = f.readlines()[-1]
    return last_line

def threadWrite(s):
    with open(result_file, "a+") as f:
        f.write("%s\n" % (s))

def threadWait(cond, item_avail_list):
    with cond:
        while not item_avail_list[0]:
            cond.wait()
        item_avail_list[0] = False

def rlockGetState(rlock):
    # Hacky solution without access to private lock attributes
    state_str = str(rlock)
    try:
        isLock = (re.search("<(unlocked|locked) ", state_str)[1]) == 'locked'
    except:
        raise Exception('Incorrect parsing')
    owner = int(re.search("owner=(\d+) ", state_str)[1]) if "owner=" in state_str else 0
    count = int(re.search("count=(\d+) ", state_str)[1]) if "count=" in state_str else 0
    return (isLock, owner, count)

def conditionGetState(cond):
    # Hacky solution without access to private cond attributes
    state_str = str(cond)
    try:
        isLock = (re.search("\(<(unlocked|locked) ", state_str)[1]) == 'locked'
        waiting = int(re.search(">, (\d+)\)>", state_str)[1])
    except:
        print("ERR: " + state_str)
        raise Exception('Incorrect parsing')
    owner = int(re.search("owner=(\d+) ", state_str)[1]) if "owner=" in state_str else 0
    count = int(re.search("count=(\d+) ", state_str)[1]) if "count=" in state_str else 0
    return (isLock, owner, count, waiting)

class Test(helper.PickleTest):
    def test_thread(self):
        t = self.loads(self.obj['t'])
        self.assertFalse(t.daemon)
        t.start()
        t.join()
        self.assertEqual(checkLastLine(), "Thread simple\n")

    def test_thread_daemon(self):
        t = self.loads(self.obj['t'])
        self.assertTrue(t.daemon)
        t.start()
        t.join()
        self.assertEqual(checkLastLine(), "Thread daemon\n")

    def test_lock(self):
        lock = self.loads(self.obj['l'])
        lock.acquire()
        self.assertTrue(lock.locked())
        lock.release()
        self.assertTrue(not lock.locked())

    def test_rlock(self):
        lock = self.loads(self.obj['l'])
        thisThread = threading.get_ident()
        self.assertEqual(rlockGetState(lock), (False, 0, 0))
        self.fail("Unable to acquire lock object")
        # The lock.acquire blocks forever even though it is unlocked.
        lock.acquire()
        self.assertEqual(rlockGetState(lock), (True, thisThread, 1))
        lock.acquire()
        self.assertEqual(rlockGetState(lock), (True, thisThread, 2))
        lock.release()
        self.assertEqual(rlockGetState(lock), (True, thisThread, 1))
        lock.release()
        self.assertEqual(rlockGetState(lock), (False, 0, 0))

    @helper.PickleTest.setFlag(helper.ResultCode.CONDITION, "Fail when using RLock")
    def test_condition(self):
        thisThread = threading.get_ident()
        cond = self.loads(self.obj['c'])
        self.assertEqual(conditionGetState(cond), (False, 0, 0, 0))
        item_avail_list = [False]
        t = threading.Thread(target=threadWait, args=(cond, item_avail_list), daemon=True)
        t.start()
        time.sleep(1) # Wait for the thread to enter cond.wait()
        self.assertEqual(conditionGetState(cond), (False, 0, 0, 1))
        cond.acquire()
        item_avail_list[0] = True
        cond.notify()
        self.assertEqual(conditionGetState(cond), (True, 0, 0, 0))
        cond.release()
        t.join()
        self.assertTrue(not item_avail_list[0])

    def test_semaphore(self):
        sem = self.loads(self.obj['s'])
        res = sem.acquire(blocking=False)
        self.assertTrue(res)
        self.assertEqual(sem._value, 1)
        res = sem.acquire(blocking=False)
        self.assertTrue(res)
        self.assertEqual(sem._value, 0)
        res = sem.acquire(blocking=False)
        self.assertFalse(res)
        self.assertEqual(sem._value, 0)
        sem.release()
        self.assertEqual(sem._value, 1)
        sem.release()
        self.assertEqual(sem._value, 2)

    def test_event(self):
        ev = self.loads(self.obj['ev'])
        self.assertTrue(not ev.is_set())
        ev.set()
        self.assertTrue(ev.is_set())
        # Test that wait can still work
        self.assertTrue(ev.wait(0.1))
        ev.clear()
        self.assertTrue(not ev.is_set())

    def test_timer(self):
        t = self.loads(self.obj['t'])
        self.assertEqual(t.interval, 1)
        self.assertTrue(not t.is_alive())
        t.start()
        self.assertTrue(t.is_alive())
        time.sleep(2)
        self.assertTrue(not t.is_alive())
        self.assertEqual(checkLastLine(), "Timer\n")

    def test_barrier(self):
        threadWrite("Barrier 1")
        b = self.loads(self.obj['b'])
        def threadWithBarrierAndSleepThenWrite(dur, s):
            time.sleep(dur)
            b.wait()
            with open(result_file, "a+") as f:
                f.write("%s\n" % (s))
        self.assertEqual(checkLastLine(), "Barrier 1\n")
        t1 = threading.Thread(target=threadWithBarrierAndSleepThenWrite, args=(1, "Barrier 2"), daemon=True)
        t1.start()
        self.assertEqual(checkLastLine(), "Barrier 1\n")
        t2 = threading.Thread(target=threadWithBarrierAndSleepThenWrite, args=(0, "Barrier 3"), daemon=True)
        t2.start()
        t1.join()
        t2.join()
        lastLine = checkLastLine()
        self.assertTrue((lastLine == "Barrier 2\n") or (lastLine == "Barrier 3\n"))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()