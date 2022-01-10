#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Builtin types and objects
Ref: https://docs.python.org/3/library/stdtypes.html
- Numeric Types — int, float, complex
- Iterator Types - Iterator object
- Generator Types [Skip, test along with generator function]
- Sequence Types — list, tuple, range
- Text Sequence Type — str
- Binary Sequence Types — bytes, bytearray, memoryview
- Set Types — set, frozenset
- Mapping Types — dict
- Context Manager Types [Skip, test in function testset]
- Generic Alias Type
- Code object
- Type objects
- Null object
- Ellipsis object
- NotImplemented object
- Boolean Values
Ref: https://docs.python.org/3/library/functions.html
- Property object [Skip, test in class testset]
- Slice object
- Proxy object [Skip until proper use case is decided]
- Mappingproxy (DictProxy by dill)
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import types
class Test(helper.PickleTest):
    def test_numeric(self):
        num1 = 185723422146583
        self.assertEqual(num1, 185723422146583)
        self.assertIsInstance(num1, int)
        self.obj['n1'] = self.dumps(num1)

        num2 = 0.025
        self.assertEqual(num2, 0.025)
        self.assertIsInstance(num2, float)
        self.obj['n2'] = self.dumps(num2)

        num3 = complex(123, 321)
        self.assertEqual(num3, complex(123, 321))
        self.assertIsInstance(num3, complex)
        self.obj['n3'] = self.dumps(num3)

    def test_iterator_object(self):
        seq1 = [1,2,3,4,5]
        it1 = iter(seq1)
        self.obj['it1'] = self.dumps(it1)
        self.assertEqual(next(it1), 1)
        self.assertEqual(next(it1), 2)
        self.assertEqual(next(it1), 3)

        it2 = iter(seq1)
        next(it2)
        next(it2)
        self.obj['it2'] = self.dumps(it2)
        self.assertEqual(next(it2), 3)
        self.assertEqual(next(it2), 4)

    def test_sequence(self):
        seq1 = [1,2,3,4,5]
        self.assertEqual(seq1, [1,2,3,4,5])
        self.assertIsInstance(seq1, list)
        self.obj['s1'] = self.dumps(seq1)

        seq2 = (1,2,3,4,5)
        self.assertEqual(seq2, (1,2,3,4,5))
        self.assertIsInstance(seq2, tuple)
        self.obj['s2'] = self.dumps(seq2)

        seq3 = range(1,6)
        self.assertEqual(seq3, range(1,6))
        self.assertIsInstance(seq3, range)
        self.obj['s3'] = self.dumps(seq3)

    def test_text(self):
        text1 = "hello WoRlD"
        self.assertEqual(text1, "hello WoRlD")
        self.obj['t1'] = self.dumps(text1)
        self.assertIsInstance(text1, str)

    def test_binary_sequence(self):
        bytes1 = bytes.fromhex('2Ef0 F1f2 ')
        self.assertEqual(bytes1, b"\x2E\xF0\xF1\xF2")
        self.assertIsInstance(bytes1, bytes)
        self.obj['b1'] = self.dumps(bytes1)

        bytes2 = bytearray.fromhex('2Ef0 F1f2 ')
        self.assertEqual(bytes2, b"\x2E\xF0\xF1\xF2")
        self.assertIsInstance(bytes2, bytearray)
        self.obj['b2'] = self.dumps(bytes2)

    def test_memoryview(self):
        bytes3 = memoryview(b"abcdefg")
        self.assertEqual(bytes3, b"abcdefg")
        with self.memTest():
            self.assertIsInstance(bytes3, memoryview)
        self.obj['mem1'] = self.dumps(bytes3)

    def test_set(self):
        set1 = set([1,2,1,3,1.0,10])
        self.assertEqual(set1, set([1,2,1,3,1.0,10]))
        self.assertIsInstance(set1, set)
        self.obj['s1'] = self.dumps(set1)

        set2 = frozenset([1,2,1,3,1.0,10])
        self.assertEqual(set2, frozenset([1,2,1,3,1.0,10]))
        self.assertIsInstance(set2, frozenset)
        self.obj['s2'] = self.dumps(set2)

    def test_dict(self):
        dict1 = {"k1": 1,
            "k2": "val",
            "k3": {"kk1": "minival"}
        }
        self.assertEqual(dict1, {"k1": 1, "k2": "val", "k3": {"kk1": "minival"}})
        self.assertIsInstance(dict1, dict)
        self.obj['d1'] = self.dumps(dict1)

    def test_generic_alias_type(self):
        if sys.version_info[0] == 3 and sys.version_info[1] < 9:
            from typing import Dict
            aliasType1 = Dict[str, str]
            self.assertEqual(aliasType1, Dict[str, str])
        else:
            aliasType1 = dict[str, str]
            self.assertEqual(aliasType1, dict[str, str])
        self.obj['at1'] = self.dumps(aliasType1)

    def test_code_object(self):
        ldict = {}
        code_obj = compile("x = \"Test code\"", "<string>", "exec")
        exec(code_obj, globals(), ldict)
        self.assertEqual(ldict["x"], "Test code")
        self.obj['c'] = self.dumps(code_obj)

    def test_type_object(self):
        type1 = int
        self.assertIsInstance(type1, type)
        self.assertEqual(type1, int)
        self.assertEqual(type1(17), 17)
        self.obj['t1'] = self.dumps(type1)

        type2 = types.LambdaType
        self.assertIsInstance(type2, type)
        self.assertEqual(type2, types.LambdaType)
        self.obj['t2'] = self.dumps(type2)

    def test_null_object(self):
        null_obj = None
        self.assertTrue(null_obj is None)
        self.obj['n'] = self.dumps(null_obj)

    def test_ellipsis_object(self):
        elp_obj = ...
        self.assertEqual(elp_obj, Ellipsis)
        self.obj['e'] = self.dumps(elp_obj)

    def test_NotImplemented_object(self):
        ni_obj = NotImplemented
        self.assertEqual(ni_obj, NotImplemented)
        self.obj['ni'] = self.dumps(ni_obj)

    def test_boolean_values(self):
        t = True
        self.assertEqual(t, True)
        self.obj['t'] = self.dumps(t)
        
        f = False
        self.assertEqual(f, False)
        self.obj['f'] = self.dumps(f)

    def test_slice_object(self):
        arr = [1,2,3,4,5,6,7,8,9,10]
        sl = slice(0,6,2)
        self.assertEqual(arr[sl], [1,3,5])
        self.obj['sl'] = self.dumps(sl)

    def test_mappingproxy(self):
        d = {'a': 13, 'b': 29}
        m = types.MappingProxyType(d)
        self.obj['d'] = self.dumps(d)
        self.obj['m'] = self.dumps(m)
        self.assertEqual(m['a'], 13)
        self.assertEqual(m['b'], 29)
        with self.memTest():
            d['a'] = 31
            self.assertEqual(m['a'], 31)
            self.assertIsInstance(m, types.MappingProxyType)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()