#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

class Test(helper.PickleTest):
    def test_closure_direct_recursive(self):
        self.assertEqual(self.loads(self.obj['c1'])(150), 9)
        self.assertEqual(self.loads(self.obj['f1'])()(150), 9)

    def test_closure_indirect_recursive(self):
        self.assertEqual(self.loads(self.obj['c1'])(150), 4)
        self.assertEqual(self.loads(self.obj['f1'])()(150), 4)
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()