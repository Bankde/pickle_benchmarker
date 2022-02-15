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
    def test_lock_running(self):
        lock = self.loads(self.obj['l'])
        self.assertTrue(lock.locked())
        lock.release()
        self.assertTrue(not lock.locked())

    def test_rlock_running(self):
        thisThread = threading.get_ident()
        lock = self.loads(self.obj['l'])
        state = self.loads(self.obj['state'])
        self.assertTrue(lock.acquire())
        self.assertEqual(rlockGetState(lock), (True, state[1], 3))
        lock.release()
        self.assertEqual(rlockGetState(lock), (True, state[1], 2))
        lock.release()
        self.assertEqual(rlockGetState(lock), (True, state[1], 1))
        lock.release()
        self.assertEqual(rlockGetState(lock), (False, 0, 0))

    def test_semaphore_running(self):
        sem = self.loads(self.obj['s'])
        self.assertEqual(sem._value, 0)
        res = sem.acquire(blocking=False)
        self.assertFalse(res)
        self.assertEqual(sem._value, 0)
        sem.release()
        self.assertEqual(sem._value, 1)
        sem.release()
        self.assertEqual(sem._value, 2)

    def test_event_running(self):
        ev = self.loads(self.obj['ev'])
        self.assertTrue(ev.is_set())
        # Test that wait can still work
        self.assertTrue(ev.wait(0.1))
        ev.clear()
        self.assertTrue(not ev.is_set())

    def test_barrier_running(self):
        threadWrite("Barrier running 1")
        def threadWithBarrierAndSleepThenWrite(dur, s):
            time.sleep(dur)
            b.wait()
            with open(result_file, "a+") as f:
                f.write("%s\n" % (s))
        self.assertEqual(checkLastLine(), "Barrier running 1\n")
        t1 = threading.Thread(target=threadWithBarrierAndSleepThenWrite, args=(1, "Barrier running 2"), daemon=True)
        t1.start()
        self.assertEqual(checkLastLine(), "Barrier running 1\n")
        b = self.loads(self.obj['b']) # This is weird, shouldn't work.
        t2 = threading.Thread(target=threadWithBarrierAndSleepThenWrite, args=(0, "Barrier running 3"), daemon=True)
        t2.start()
        t1.join()
        t2.join()
        lastLine = checkLastLine()
        self.assertTrue((lastLine == "Barrier running 2\n") or (lastLine == "Barrier running 3\n"))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()