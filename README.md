# pickle_benchmarker

Run the test

```
python test.py
```

The raw result will be in result.json in json format.  
The result_summary.txt provides the summary table of supported object types.

This testsuite uses Python subprocess to run so make sure the environment is correct (e.g. Python version, dill, cloudpickle) during the test.  
If run in the IDE, make sure the IDE uses the correct Python version throughout the test.
