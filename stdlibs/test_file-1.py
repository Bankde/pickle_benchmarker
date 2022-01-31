#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# IO
Ref: https://docs.python.org/3/library/io.html
- Read/Write with path to files: text, binary IO
- In-memory text streams - StringIO, ByteIO object
- Non-zero pointer IO object
- IO object without actual file
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import io

file_read_name = os.path.join(sys.path[0], "./dependencies", "test_file_read.txt")
file_write_name = os.path.join(sys.path[0], "./dependencies", "test_file_write.tmp")
file_temp_name = os.path.join(sys.path[0], "./dependencies", "test_file_tmp.tmp")
file_temp_name_2 = os.path.join(sys.path[0], "./dependencies", "test_file_tmp_2.tmp")
open(file_write_name, "w+").close() # Reset the file
with open(file_temp_name, "w+") as f: # Reset the file
    f.write("Line 1\nLine 2\nLine 3\n")
with open(file_temp_name_2, "w+") as f: # Reset the file
    f.write("Line 1\nLine 2\nLine 3\n")

def getLastLine(file):
    with open(file, "r") as f:
        last_line = f.readlines()[-1]
    return last_line

class Test(helper.PickleTest):
    def test_read_IO_with_path(self):
        with open(file_read_name, "r", encoding="utf-8") as fr1:
            self.obj['fr1'] = self.dumps(fr1)
            self.assertEqual(fr1.readline(), "Test2Data 1st line\n")

    def test_read_IO_binary_with_path(self):
        with open(file_read_name, "rb") as fr1:
            self.obj['fr1'] = self.dumps(fr1)
            self.assertEqual(fr1.readline(), b"Test2Data 1st line\n")
        
    def test_write_IO_with_path(self):
        with open(file_write_name, "a", encoding="utf-8") as fw1:
            self.obj['fw1'] = self.dumps(fw1)
            fw1.write("Hello 1\n")
        self.assertEqual(getLastLine(file_write_name), "Hello 1\n")

    def test_write_IO_binary_with_path(self):
        with open(file_write_name, "ab") as fw1:
            self.obj['fw1'] = self.dumps(fw1)
            fw1.write(b"Hello 2\n")
        self.assertEqual(getLastLine(file_write_name), "Hello 2\n")
        
    def test_in_memory_stream(self):
        with io.StringIO("test 2 in memory stream text data") as ms1:
            self.obj['ms1'] = self.dumps(ms1)
            self.assertEqual(ms1.readline(), "test 2 in memory stream text data")
        with io.BytesIO(b"test 2 in memory stream byte data") as ms2:
            self.obj['ms2'] = self.dumps(ms2)
            self.assertEqual(ms2.readline(), b"test 2 in memory stream byte data")

    def test_non_zero_ptr_IO_object(self):
        with open(file_read_name, "r", encoding="utf-8") as fr1:
            _ = fr1.readline()
            self.obj['fr1'] = self.dumps(fr1)
            self.assertEqual(fr1.readline(), "Test2Data 2nd line\n")

    def test_non_zero_ptr_IO_binary_object(self):
        with open(file_read_name, "rb") as fr1:
            _ = fr1.readline()
            self.obj['fr1'] = self.dumps(fr1)
            self.assertEqual(fr1.readline(), b"Test2Data 2nd line\n")

    def test_read_IO_without_file(self):
        with open(file_temp_name, "r", encoding="utf-8") as f:
            self.obj['f'] = self.dumps(f)
            self.assertEqual(f.readline(), "Line 1\n")
            self.assertEqual(f.readline(), "Line 2\n")
        os.remove(file_temp_name)

    @unittest.skipIf(helper.pickle.__name__ != "dill", "Only test for dill")
    def test_dill_file_fmode_non_zero_ptr_IO_object(self):
        with open(file_read_name, "r", encoding="utf-8") as fr1:
            _ = fr1.readline()
            self.obj['fr1'] = self.dumps(fr1, fmode=helper.pickle.FILE_FMODE)
            self.assertEqual(fr1.readline(), "Test2Data 2nd line\n")

    @unittest.skipIf(helper.pickle.__name__ != "dill", "Only test for dill")
    def test_dill_read_IO_without_file(self):
        with open(file_temp_name_2, "r", encoding="utf-8") as f:
            self.obj['f'] = self.dumps(f, fmode=helper.pickle.CONTENTS_FMODE)
            self.assertEqual(f.readline(), "Line 1\n")
            self.assertEqual(f.readline(), "Line 2\n")
        os.remove(file_temp_name_2)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()