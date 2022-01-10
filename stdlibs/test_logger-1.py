#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
###### Description ######
# Logging
- Logger object
- Handler object
- Formatter object
- Filter object
- LogRecord object
- LoggerAdapter object
###### End of Description ######
'''

import sys, os
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))
import helper

########## Code Here ##########

from io import StringIO
import logging

'''
Developer should be careful while developing the test.
The logging module is singleton throughout the process so getLogger may return previously used logger
'''
def removeAllHandlers(logger):
    for handler in logger.handlers:
        logger.removeHandlers(handler)

def prepareLoggerWithStreamHandler(loggerName, handler=None):
    if handler == None:
        stream = StringIO()
        handler = logging.StreamHandler(stream)
    else:
        stream = handler.stream
    logger = logging.getLogger(loggerName)
    removeAllHandlers(logger)
    logger.addHandler(handler)
    return logger, handler, stream

class Test(helper.PickleTest):
    def test_logger_object(self):
        '''
        Design the test based on https://docs.python.org/3/library/logging.html
        > Loggers should NEVER be instantiated directly, 
        > but always through the module-level function logging.getLogger(name). 
        > Multiple calls to getLogger() with the same name will always return a reference to the same Logger object.
        '''
        l1, handler, stream = prepareLoggerWithStreamHandler("logObj")
        self.obj['l'] = self.dumps(l1)
        l2 = logging.getLogger("logObj")
        self.assertTrue(l1 is l2)
        l1.error("Test error")
        self.assertEqual(stream.getvalue().strip(), "Test error")

    def test_logger_object_with_hierachy(self):
        l1, handler1, stream1 = prepareLoggerWithStreamHandler("logObjHrchy")
        l2, handler2, stream2 = prepareLoggerWithStreamHandler("logObjHrchy.mini")
        self.obj['l1'] = self.dumps(l1)
        self.obj['l2'] = self.dumps(l2)
        l2.error("Test hierachy error")
        self.assertEqual(stream1.getvalue().strip(), "Test hierachy error")
        self.assertEqual(stream2.getvalue().strip(), "Test hierachy error")

    def test_handler(self):
        l1, handler, stream = prepareLoggerWithStreamHandler("logHandler")
        self.obj['h1'] = self.dumps(handler)
        l1.error("Test handler")
        self.assertEqual(stream.getvalue().strip(), "Test handler")

    def test_formatter(self):
        fmt = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        self.obj['f1'] = self.dumps(fmt)
        l1, handler, stream = prepareLoggerWithStreamHandler("logFmt")
        handler.setFormatter(fmt)
        l1.error("Test fmt")
        self.assertEqual(stream.getvalue().strip(), "logFmt - ERROR - Test fmt")

    def test_filter(self):
        filter = logging.Filter('logFilter')
        self.obj['f1'] = self.dumps(filter)
        l1, handler1, stream1 = prepareLoggerWithStreamHandler("logFilter")
        l2, handler2, stream2 = prepareLoggerWithStreamHandler("logFilterNot")
        handler1.addFilter(filter)
        handler2.addFilter(filter)
        l1.error("Test filter")
        l2.error("Test filter")
        self.assertEqual(stream1.getvalue().strip(), "Test filter")
        self.assertEqual(stream2.getvalue().strip(), "")

    def test_logRecord(self):
        # We use this trick to get record object without requiring attrdict
        rec = None
        def filter(record):
            nonlocal rec
            rec = record
            return True
        l1, handler1, stream1 = prepareLoggerWithStreamHandler("logRecord")
        l1.addFilter(filter)
        l1.error("Test record")
        self.assertEqual(stream1.getvalue().strip(), "Test record")
        self.assertTrue(rec != None)
        self.obj['r'] = self.dumps(rec)
        self.assertEqual(rec.message, "Test record")
        self.assertEqual(rec.levelno, 40)

########## End of Code ##########

if __name__ == "__main__":
    unittest.main()