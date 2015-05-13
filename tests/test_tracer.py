#! /usr/bin/env python
# Copyright (C) 2015 Federico (phretor) Maggi
# This software may be modified and distributed under the terms
# of the MIT license. See the LICENSE file for details.

import os
import sys
import time
import unittest
import subprocess

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYZER_FOLDER = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..', 'analyzer', 'darwin'))

sys.path.append(ANALYZER_FOLDER)

from lib.api.tracer import DTrace

class TestTracer(unittest.TestCase):
    def setUp(self):
        build_target(self.current_target())

    def tearDown(self):
        return
        cleanup_target(self.current_target())

    def current_target(self):
        return self._testMethodName

    def test_tracer(self):
        tracer = DTrace()
        path = executable_name_for_target(self.current_target())

        # just making sure
        self.assertTrue(os.path.isfile(path))

        tracer.execute(path=path, args=[self.current_target()])

        # to test the non-blocking behavior of the tracer, wait at least
        # 5s to make sure that the program has completed
        time.sleep(7)

        truth_out = ("""Entering main
        Hello 0 %(target)s
        Hello 1 %(target)s
        Hello 2 %(target)s
        Hello 3 %(target)s
        Hello 4 %(target)s""" % {'target': self.current_target() }).split('\n')

        with open(tracer._target_stdout_file) as out:
            for i, line in enumerate(out):
                ll = line.strip()
                tt = truth_out[i].strip()
                self.assertEqual(tt, ll)

        truth_err = ("""The hell is here 0 %(target)s
        The hell is here 1 %(target)s
        The hell is here 2 %(target)s
        The hell is here 3 %(target)s
        The hell is here 4 %(target)s""" % {'target': self.current_target() }).split('\n')

        with open(tracer._target_stderr_file) as err:
            for i, line in enumerate(err):
                ll = line.strip()
                tt = truth_err[i].strip()
                self.assertEqual(tt, ll)

        with open(tracer._trace_file) as trc:
            blob = ''.join([u for u in trc])
            for to in truth_out:
                self.assertIn(to.strip(), blob)
            for te in truth_err:
                self.assertIn(te.strip(), blob)

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

if __name__ == '__main__':
    unittest.main()
