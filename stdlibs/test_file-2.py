#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

file_write_name = os.path.join(sys.path[0], "./dependencies", "test_file_write.tmp")
def getLastLine(file):
    with open(file, "r") as f:
        last_line = f.readlines()[-1]
    return last_line

class Test(helper.PickleTest):
    def test_read_IO_with_path(self):
        with self.loads(self.obj['fr1']) as fr1:
            self.assertEqual(fr1.readline(), "Test2Data 1st line\n")

    def test_read_IO_binary_with_path(self):
        with self.loads(self.obj['fr1']) as fr1:
            self.assertEqual(fr1.readline(), b"Test2Data 1st line\n")
        
    def test_write_IO_with_path(self):
        with self.loads(self.obj['fw1']) as fw1:
            fw1.write("Hello 1\n")
        self.assertEqual(getLastLine(file_write_name), "Hello 1\n")

    def test_write_IO_binary_with_path(self):
        with self.loads(self.obj['fw1']) as fw1:
            fw1.write(b"Hello 2\n")
        self.assertEqual(getLastLine(file_write_name), "Hello 2\n")
        
    def test_in_memory_stream(self):
        with self.loads(self.obj['ms1']) as ms1:
            self.assertEqual(ms1.readline(), "test 2 in memory stream text data")
        with self.loads(self.obj['ms2']) as ms2:
            self.assertEqual(ms2.readline(), b"test 2 in memory stream byte data")

    def test_non_zero_ptr_IO_object(self):
        with self.loads(self.obj['fr1']) as fr1:
            self.assertEqual(fr1.readline(), "Test2Data 2nd line\n")

    def test_non_zero_ptr_IO_binary_object(self):
        with self.loads(self.obj['fr1']) as fr1:
            self.assertEqual(fr1.readline(), b"Test2Data 2nd line\n")

    def test_read_IO_without_file(self):
        with self.loads(self.obj['f']) as f:
            self.assertEqual(f.readline(), "Line 1\n")
            self.assertEqual(f.readline(), "Line 2\n")

    @unittest.skipIf(helper.pickle.__name__ != "dill", "Only test for dill")
    def test_dill_file_fmode_non_zero_ptr_IO_object(self):
        with self.loads(self.obj['fr1']) as fr1:
            self.assertEqual(fr1.readline(), "Test2Data 2nd line\n")

    @unittest.skipIf(helper.pickle.__name__ != "dill", "Only test for dill")
    def test_dill_read_IO_without_file(self):
        with self.loads(self.obj['f']) as f:
            self.assertEqual(f.readline(), "Line 1\n")
            self.assertEqual(f.readline(), "Line 2\n")

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()