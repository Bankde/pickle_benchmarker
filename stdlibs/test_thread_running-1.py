#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# On-running Threading
- Lock object
- RLock object
- Condition object
- Semaphore object
- Event object
- Barrier object
# Not test (because they use _thread.start_new_thread)
- Thread object
- Timer object
###### End of Description ######
'''

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
        lock = threading.Lock()
        lock.acquire()
        self.assertTrue(lock.locked())
        self.obj['l'] = self.dumps(lock)
        lock.release()
        self.assertTrue(not lock.locked())

    def test_rlock_running(self):
        lock = threading.RLock()
        thisThread = threading.get_ident()
        self.assertEqual(rlockGetState(lock), (False, 0, 0))
        self.assertTrue(lock.acquire())
        self.assertEqual(rlockGetState(lock), (True, thisThread, 1))
        self.assertTrue(lock.acquire())
        self.assertEqual(rlockGetState(lock), (True, thisThread, 2))
        self.obj['l'] = self.dumps(lock)
        self.obj['state'] = self.dumps(rlockGetState(lock)) # (True, thisThread, 2)
        self.assertTrue(lock.acquire())
        self.assertEqual(rlockGetState(lock), (True, thisThread, 3))
        lock.release()
        self.assertEqual(rlockGetState(lock), (True, thisThread, 2))
        lock.release()
        self.assertEqual(rlockGetState(lock), (True, thisThread, 1))
        lock.release()
        self.assertEqual(rlockGetState(lock), (False, 0, 0))

    def test_semaphore_running(self):
        sem = threading.Semaphore(value=2)
        res = sem.acquire(blocking=False)
        self.assertTrue(res)
        self.assertEqual(sem._value, 1)
        res = sem.acquire(blocking=False)
        self.assertTrue(res)
        self.assertEqual(sem._value, 0)
        self.obj['s'] = self.dumps(sem)
        res = sem.acquire(blocking=False)
        self.assertFalse(res)
        self.assertEqual(sem._value, 0)
        sem.release()
        self.assertEqual(sem._value, 1)
        sem.release()
        self.assertEqual(sem._value, 2)

    def test_event_running(self):
        ev = threading.Event()
        self.assertTrue(not ev.is_set())
        ev.set()
        self.assertTrue(ev.is_set())
        self.obj['ev'] = self.dumps(ev)
        # Test that wait can still work
        self.assertTrue(ev.wait(0.1))
        ev.clear()
        self.assertTrue(not ev.is_set())

    def test_barrier_running(self):
        threadWrite("Barrier running 1")
        b = threading.Barrier(2)
        def threadWithBarrierAndSleepThenWrite(dur, s):
            time.sleep(dur)
            b.wait()
            with open(result_file, "a+") as f:
                f.write("%s\n" % (s))
        self.assertEqual(checkLastLine(), "Barrier running 1\n")
        t1 = threading.Thread(target=threadWithBarrierAndSleepThenWrite, args=(1, "Barrier running 2"), daemon=True)
        t1.start()
        self.assertEqual(checkLastLine(), "Barrier running 1\n")
        self.obj['b'] = self.dumps(b) # This is weird, shouldn't work.
        t2 = threading.Thread(target=threadWithBarrierAndSleepThenWrite, args=(0, "Barrier running 3"), daemon=True)
        t2.start()
        t1.join()
        t2.join()
        lastLine = checkLastLine()
        self.assertTrue((lastLine == "Barrier running 2\n") or (lastLine == "Barrier running 3\n"))

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()