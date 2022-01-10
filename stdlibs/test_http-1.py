#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# HTTP requests module
- urllib
- requests
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

import urllib
import requests

test_url = "https://example.com"
data = [
    b'<!doctype html>\n',
    b'<html>\n',
    b'<head>\n',
    b'    <title>Example Domain</title>\n'
]

class Test(helper.PickleTest):
    def test_urllib(self):
        r = urllib.request.urlopen(test_url)
        self.obj['r'] = self.dumps(r)
        self.assertEqual(r.status, 200)
        self.assertEqual(r.url.strip('/'), test_url)
        self.assertEqual(r.readline(), data[0])
        self.assertEqual(r.readline(), data[1])
        self.assertEqual(r.readline(), data[2])
        self.assertEqual(r.readline(), data[3])

    def test_requests(self):
        r = requests.get(test_url)
        self.obj['r'] = self.dumps(r)
        self.assertIsInstance(r, requests.Response)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.url.strip('/'), test_url)
        it = r.iter_lines()
        self.assertEqual(it.__next__(), data[0].strip(b'\n'))
        self.assertEqual(it.__next__(), data[1].strip(b'\n'))
        self.assertEqual(it.__next__(), data[2].strip(b'\n'))
        self.assertEqual(it.__next__(), data[3].strip(b'\n'))
        it.close()
        
########## End of Code ##########

if __name__ == "__main__":
    unittest.main()