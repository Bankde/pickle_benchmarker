#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import collections

class Test(helper.PickleTest):
    def test_namedtuple_class(self):
        Point = self.loads(self.obj['c'])
        self.assertEqual(Point.__class__.__name__, 'type')
        p = Point(11, y=22)
        self.assertEqual(p.x, 11)
        self.assertEqual(p.y, 22)
        self.assertEqual(p.__class__.__name__, 'Point')

    def test_namedtuple_instance(self):
        p = self.loads(self.obj['p'])
        self.assertEqual(p.x, 11)
        self.assertEqual(p.y, 22)
        self.assertEqual(p.__class__.__name__, 'Point')

    def test_deque(self):
        q = self.loads(self.obj['q'])
        self.assertIsInstance(q, collections.deque)
        self.assertEqual(list(q), [1,2,3,4])
        self.assertEqual(q.popleft(), 1)
        q.appendleft(5)
        self.assertEqual(list(q), [5,2,3,4])

    def test_chainmap(self):
        d1 = self.loads(self.obj['d1'])
        d2 = self.loads(self.obj['d2'])
        m = self.loads(self.obj['m'])
        self.assertIsInstance(m, collections.ChainMap)
        self.assertEqual(m.maps, [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}])
        with self.memTest():
            d1["a"] = 10
            self.assertEqual(m.maps, [{'a': 10, 'b': 2}, {'c': 3, 'd': 4}])

    def test_counter(self):
        c = self.loads(self.obj['c'])
        self.assertIsInstance(c, collections.Counter)
        self.assertDictEqual(c, {'h': 1, 'e': 1, 'l': 3, 'o':2, ' ': 1, 'w': 1, 'r': 1, 'd': 1})

    def test_ordereddict(self):
        d = self.loads(self.obj['d'])
        self.assertIsInstance(d, collections.OrderedDict)
        self.assertEqual(list(d.keys()), ['a', 'b', 'c', 'd', 'e'])
        d.move_to_end('b')
        self.assertEqual(list(d.keys()), ['a', 'c', 'd', 'e', 'b'])

    def test_defaultdict(self):
        d = self.loads(self.obj['d'])
        self.assertIsInstance(d, collections.defaultdict)
        d["number"].add(1)
        self.assertIsInstance(d["number"], set)
        self.assertTrue("a" in d["alphabet"])
        self.assertTrue(1 in d["number"])

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()