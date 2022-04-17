#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import types
class Test(helper.PickleTest):
    def test_numeric(self):
        num1 = self.loads(self.obj['n1'])
        self.assertEqual(num1, 185723422146583)
        self.assertIsInstance(num1, int)

        num2 = self.loads(self.obj['n2'])
        self.assertEqual(num2, 0.025)
        self.assertIsInstance(num2, float)

        num3 = self.loads(self.obj['n3'])
        self.assertEqual(num3, complex(123, 321))
        self.assertIsInstance(num3, complex)

    def test_iterator_object(self):
        seq1 = [1,2,3,4,5]
        it1 = self.loads(self.obj['it1'])
        self.assertEqual(next(it1), 1)
        self.assertEqual(next(it1), 2)
        self.assertEqual(next(it1), 3)

        it2 = self.loads(self.obj['it2'])
        self.assertEqual(next(it2), 3)
        self.assertEqual(next(it2), 4)

    def test_sequence(self):
        seq1 = self.loads(self.obj['s1'])
        self.assertEqual(seq1, [1,2,3,4,5])
        self.assertIsInstance(seq1, list)

        seq2 = self.loads(self.obj['s2'])
        self.assertEqual(seq2, (1,2,3,4,5))
        self.assertIsInstance(seq2, tuple)

        seq3 = self.loads(self.obj['s3'])
        self.assertEqual(seq3, range(1,6))
        self.assertIsInstance(seq3, range)

    def test_text(self):
        text1 = self.loads(self.obj['t1'])
        self.assertEqual(text1, "hello WoRlD")
        self.assertIsInstance(text1, str)

    def test_binary_sequence(self):
        bytes1 = self.loads(self.obj['b1'])
        self.assertEqual(bytes1, b"\x2E\xF0\xF1\xF2")
        self.assertIsInstance(bytes1, bytes)

        bytes2 = self.loads(self.obj['b2'])
        self.assertEqual(bytes2, b"\x2E\xF0\xF1\xF2")
        self.assertIsInstance(bytes2, bytearray)

    def test_memoryview(self):
        bytes3 = self.loads(self.obj['mem1'])
        self.assertEqual(bytes3, b"abcdefg")
        with self.memTest():
            self.assertIsInstance(bytes3, memoryview)

    def test_set(self):
        set1 = self.loads(self.obj['s1'])
        self.assertEqual(set1, set([1,2,1,3,1.0,10]))
        self.assertIsInstance(set1, set)
        
        set2 = self.loads(self.obj['s2'])
        self.assertEqual(set2, frozenset([1,2,1,3,1.0,10]))
        self.assertIsInstance(set2, frozenset)

    def test_dict(self):
        dict1 = self.loads(self.obj['d1'])
        self.assertEqual(dict1, {"k1": 1, "k2": "val", "k3": {"kk1": "minival"}})
        self.assertIsInstance(dict1, dict)

    def test_generic_alias_type(self):
        aliasType1 = self.loads(self.obj['at1'])
        if sys.version_info[0] == 3 and sys.version_info[1] < 9:
            from typing import Dict
            self.assertEqual(aliasType1, Dict[str, str])
        else:
            self.assertEqual(aliasType1, dict[str, str])

    def test_code_object(self):
        ldict = {}
        code_obj = self.loads(self.obj['c'])
        exec(code_obj, globals(), ldict)
        self.assertEqual(ldict["x"], "Test code")

    def test_type_object(self):
        type1 = self.loads(self.obj['t1'])
        self.assertIsInstance(type1, type)
        self.assertEqual(type1, int)
        self.assertEqual(type1(17), 17)

        type2 = self.loads(self.obj['t2'])
        self.assertIsInstance(type2, type)
        self.assertEqual(type2, types.LambdaType)

    def test_null_object(self):
        null_obj = self.loads(self.obj['n'])
        self.assertTrue(null_obj is None)

    def test_ellipsis_object(self):
        elp_obj = self.loads(self.obj['e'])
        self.assertEqual(elp_obj, Ellipsis)

    def test_NotImplemented_object(self):
        ni_obj = self.loads(self.obj['ni'])
        self.assertEqual(ni_obj, NotImplemented)

    def test_boolean_values(self):
        t = self.loads(self.obj['t'])
        self.assertEqual(t, True)

        f = self.loads(self.obj['f'])
        self.assertEqual(f, False)

    def test_slice_object(self):
        arr = [1,2,3,4,5,6,7,8,9,10]
        sl = self.loads(self.obj['sl'])
        self.assertEqual(arr[sl], [1,3,5])

    def test_mappingproxy(self):
        d = self.loads(self.obj['d'])
        m = self.loads(self.obj['m'])
        self.assertEqual(m['a'], 13)
        self.assertEqual(m['b'], 29)
        self.assertIsInstance(m, types.MappingProxyType)
        with self.memTest():
            d['a'] = 31
            self.assertEqual(m['a'], 31)

    def test_bundled_mappingproxy(self):
        bundle = self.loads(self.obj['b'])
        self.assertEqual(bundle['m']['a'], 13)
        self.assertEqual(bundle['m']['b'], 29)
        self.assertIsInstance(bundle['m'], types.MappingProxyType)
        with self.memTest():
            bundle['d']['a'] = 31
            self.assertEqual(bundle['m']['a'], 31)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()