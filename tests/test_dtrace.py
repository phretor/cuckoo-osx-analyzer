#!/usr/bin/env python
# Copyright (C) 2015 Dmitry Rodionov
# This file is part of my GSoC'15 project for Cuckoo Sandbox:
#	http://www.cuckoosandbox.org
# This software may be modified and distributed under the terms
# of the MIT license. See the LICENSE file for details.

import os
import sys
import unittest
import subprocess

from dtrace.dtruss import *

TESTS_DIR = os.path.dirname(os. path.abspath(__file__))

# dtruss is unable to deal with paths with spaces in it,
# so we use a relative path to a target instead.
# TODO(rodionovd): we can either have our own (fixed) version of
# dtruss or just leave it as is.
class TestDtrace(unittest.TestCase):

	def setUp(self):
		build_target(self.current_target())

	def tearDown(self):
		cleanup_target(self.current_target())

	def current_target(self):
		return self._testMethodName

	def test_dtruss_helloworld(self):
		# given
		print_hello_world_syscall = ('write_nocancel', ['0x1', 'Hello, world!\\n\\0', '0xE'], '14', '0')
		# when
		output = dtruss("./tests/assets/"+self.current_target())
		#then
		self.assertIn(print_hello_world_syscall, output)

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
