#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Collections
- namedtuple class
- namedtuple instance
- deque
- ChainMap
- Counter
- OrderedDict
- defaultdict
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import collections

class Test(helper.PickleTest):
    def test_namedtuple_class(self):
        Point = collections.namedtuple('Point', ['x', 'y'])
        self.obj['c'] = self.dumps(Point)
        self.assertEqual(Point.__class__.__name__, 'type')
        p = Point(11, y=22)
        self.assertEqual(p.x, 11)
        self.assertEqual(p.y, 22)
        self.assertEqual(p.__class__.__name__, 'Point')

    def test_namedtuple_instance(self):
        Point = collections.namedtuple('Point', ['x', 'y'])
        p = Point(11, y=22)
        self.obj['p'] = self.dumps(p)
        self.assertEqual(p.x, 11)
        self.assertEqual(p.y, 22)
        self.assertEqual(p.__class__.__name__, 'Point')

    def test_deque(self):
        q = collections.deque([1,2,3,4])
        self.obj['q'] = self.dumps(q)
        self.assertIsInstance(q, collections.deque)
        self.assertEqual(list(q), [1,2,3,4])
        self.assertEqual(q.popleft(), 1)
        q.appendleft(5)
        self.assertEqual(list(q), [5,2,3,4])

    def test_chainmap(self):
        d1 = {"a":1,"b":2}
        d2 = {"c":3,"d":4}
        m = collections.ChainMap(d1, d2)
        self.obj['d1'] = self.dumps(d1)
        self.obj['d2'] = self.dumps(d2)
        self.obj['m'] = self.dumps(m)
        self.assertIsInstance(m, collections.ChainMap)
        self.assertEqual(m.maps, [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}])
        with self.memTest():
            d1["a"] = 10
            self.assertEqual(m.maps, [{'a': 10, 'b': 2}, {'c': 3, 'd': 4}])

    def test_counter(self):
        c = collections.Counter('hello world')
        self.obj['c'] = self.dumps(c)
        self.assertIsInstance(c, collections.Counter)
        self.assertDictEqual(c, {'h': 1, 'e': 1, 'l': 3, 'o':2, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

    def test_ordereddict(self):
        d = collections.OrderedDict.fromkeys("abcde")
        self.obj['d'] = self.dumps(d)
        self.assertIsInstance(d, collections.OrderedDict)
        self.assertEqual(list(d.keys()), ['a', 'b', 'c', 'd', 'e'])
        d.move_to_end('b')
        self.assertEqual(list(d.keys()), ['a', 'c', 'd', 'e', 'b'])

    def test_defaultdict(self):
        d = collections.defaultdict(set)
        d["alphabet"].add("a")
        self.obj['d'] = self.dumps(d)
        self.assertIsInstance(d, collections.defaultdict)
        d["number"].add(1)
        self.assertIsInstance(d["number"], set)
        self.assertTrue("a" in d["alphabet"])
        self.assertTrue(1 in d["number"])

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()