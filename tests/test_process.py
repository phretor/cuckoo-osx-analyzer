#! /usr/bin/env python
# Copyright (C) 2015 Federico (phretor) Maggi
# This software may be modified and distributed under the terms
# of the MIT license. See the LICENSE file for details.

import os
import sys
import time
import logging
import unittest
import subprocess

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYZER_FOLDER = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..', 'analyzer', 'darwin'))

sys.path.append(ANALYZER_FOLDER)

from lib.api.process import Process

class TestProcess(unittest.TestCase):
    def setUp(self):
        setup_logging()
        build_target(self.current_target())

    def tearDown(self):
        return
        cleanup_target(self.current_target())

    def current_target(self):
        return self._testMethodName

    def test_process(self):
        process = Process()
        path = executable_name_for_target(self.current_target())

        # just making sure
        self.assertTrue(os.path.isfile(path))

        res = process.execute(path='non_existing')
        pid = process.pid

        self.assertFalse(res)
        self.assertTrue(pid == None)

        res = process.execute(path=path, args=['first', 'second'])
        pid = process.pid

        self.assertTrue(res)
        self.assertTrue(pid != None)
        self.assertIsInstance(pid, int)

def build_target(target):
    # clang -arch x86_64 -o $target_name $target_name.c
    output = executable_name_for_target(target)
    source = sourcefile_name_for_target(target)
    subprocess.check_call(["clang", "-arch", "x86_64", "-o", output, source])

def cleanup_target(target):
    os.remove(executable_name_for_target(target))

def sourcefile_name_for_target(target):
    return "%s/assets/%s.c" % (TESTS_DIR, target)

def executable_name_for_target(target):
    return "%s/assets/%s" % (TESTS_DIR, target)

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

if __name__ == '__main__':
    unittest.main()
