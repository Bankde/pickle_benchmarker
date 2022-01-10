#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# pandas
https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html
- series
- dataFrame
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import pandas as pd

class Test(helper.PickleTest):
    def test_series(self):
        s = pd.Series([3, 6, 9], index=["a", "b", "c"], name="series test")
        self.obj["s"] = self.dumps(s)
        self.assertIsInstance(s, pd.core.series.Series)
        self.assertEqual(len(s), 3)
        self.assertEqual(s["a"], 3)
        self.assertEqual(s[0], 3)
        self.assertEqual(s.name, "series test")
        self.assertDictEqual(s.to_dict(), {'a': 3, 'b': 6, 'c': 9})
    
    def test_dataframe(self):
        d = { 
            "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
            "two": pd.Series([11.0, 12.0, 13.0], index=["a", "b", "c"]),
        }
        df = pd.DataFrame(d)
        self.obj["df"] = self.dumps(df)
        self.assertIsInstance(df, pd.core.frame.DataFrame)
        s = df["two"]
        self.assertIsInstance(s, pd.core.series.Series)
        self.assertDictEqual(s.to_dict(), {'a': 11.0, 'b': 12.0, 'c': 13.0})
        self.assertDictEqual(df.to_dict(), {'one': {'a': 1.0, 'b': 2.0, 'c': 3.0}, 'two': {'a': 11.0, 'b': 12.0, 'c': 13.0}})

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()