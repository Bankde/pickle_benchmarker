#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import subprocess
import re
from collections import defaultdict
import datetime
import json
import pandas as pd

result_file = "result.json" # Same name within the helper.py module

testSuites = [
    "functions",
    "stdlibs",
    "others"
]
pickleSuites = [
    "dill",
    "cloudpickle",
    "pickle"
]

testname_re = re.compile("test_(\w+)-(\d+).py")

# https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script
def get_git_revision_hash() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except:
        return "None"

def initResultFile():
    all_results = {}
    for p in pickleSuites:
        all_results[p] = {}
    all_results["timestamp"] = str(datetime.datetime.now())
    all_results["commit"] = get_git_revision_hash()
    all_results["pickleSuites"] = pickleSuites
    with open(result_file, "w+") as f:
        json.dump(all_results, f)

initResultFile()

errorTxt = set() # Remove duplicate error

for pickle in pickleSuites:
    new_env = os.environ
    new_env["PickleLib"] = pickle
    print("===== Testing for %s =====" % (pickle))
    for testSuite in testSuites:
        path = os.path.join(sys.path[0], testSuite)
        files = os.listdir(path)
        testsets = defaultdict(lambda: 0)
        for file in files:
            match = re.match(testname_re, file)
            if match == None:
                continue
            testsets[match.group(1)] += 1
        
        for testset in sorted(testsets.keys()):
            if testsets[testset] < 2:
                errorTxt.add("Error incomplete testset: %s %s" % (path, testset))
                continue

            testsetName = os.path.join(path, "test_" + testset)
            # Note: the "-1.py" will always be init'ed test.
            for i in range(1,testsets[testset]+1):
                try:
                    testPickle = testsetName + "-%d.py" % (i)
                    subprocess.check_output(['python', testPickle], env=new_env)
                except:
                    # We ignore the exceptions raised from the tests
                    pass

if len(errorTxt) > 0:
    print("Testsuite with error:")
    print(errorTxt)

##################################
########## SUMMARY FILE ##########
##################################

summary_file = "result_summary.txt"
testname_re = re.compile("test_(\d+)-(\d+).py")

testsuiteNameCache = {}
def getTestsuiteNameFromFile(file):
    global testsuiteNameCache
    s = file.replace("-","/").split("/")
    cur_test = s[-3]+"/"+s[-2]
    with open(file, "r") as f:
        for line in f:
            if line.startswith("###### Description ######"):
                testsuite_name = (f.readline()).strip("#\ \n")
                testsuiteNameCache[cur_test] = testsuite_name
                return testsuite_name

def getTestsuiteName(file):
    global testsuiteNameCache
    s = cur_file.replace("-","/").split("/")
    cur_test = s[-3]+"/"+s[-2]
    return testsuiteNameCache[cur_test]

with open(result_file, "r") as f:
    raw_results = json.load(f)

with open(summary_file, "w+") as f:
    f.write("Time: " + raw_results["timestamp"] + "\n")
    f.write("Commit: " + raw_results["commit"] + "\n")

result_dict = {}
for cur_pickle in raw_results["pickleSuites"]:
    result_dict[cur_pickle] = {}
    # First loop to init the dict with testsuite name
    for cur_file in raw_results[cur_pickle]:
        if cur_file.endswith("-1.py"):
            cur_testname = getTestsuiteNameFromFile(cur_file)
            if cur_testname in result_dict[cur_pickle]:
                raise Exception("Impossible flow") # Only one init file should exist.
            result_dict[cur_pickle][cur_testname] = [{} for i in range(2)] # 0/1 for init/test
    # Add the result to our result_dict
    for cur_file in raw_results[cur_pickle]:
        # Remove "msg" from raw_result
        results = {k: raw_results[cur_pickle][cur_file][k]["result"] for k in raw_results[cur_pickle][cur_file]}
        if cur_file.endswith("-1.py"):
            result_dict[cur_pickle][getTestsuiteName(cur_file)][0] = results
        else:
            # There may be several test file
            result_dict[cur_pickle][getTestsuiteName(cur_file)][1].update(results)

# Beauty print with pandas
with open(summary_file, "a+") as f:
    for testsuite in result_dict[list(result_dict.keys())[0]]:
        df_all_pickles = []
        for cur_pickle in result_dict:
            df = pd.DataFrame(data=result_dict[cur_pickle][testsuite])
            df = df.fillna(' ').T
            df = df.rename(columns={0: "Init(%s)" % (cur_pickle), 1: "Test(%s)" % (cur_pickle)})
            df_all_pickles.append(df)
        result = pd.concat(df_all_pickles, axis=1)
        f.write("===== Testsuite: %s =====\n" % (testsuite))
        f.write(str(result))
        f.write("\n")