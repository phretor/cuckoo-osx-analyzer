# Copyright (C) 2015 Federico (phretor) Maggi

import os
import logging
import tempfile
import subprocess

from lib.common.constants import D_SCRIPT

log = logging.getLogger(__name__)

class DTrace(object):
    """Simple wrapper around a DTrace script."""

    def __init__(self, d_script=D_SCRIPT):
        """Initializes the tracer.
        @param d_script: path to executable D script.
        """
        self.d_script = d_script
        self._process = None
        self._pid = None
        self._tmp = None
        self._trace_file = None
        self._target_stdout_file = None
        self._target_stderr_file = None

    def prepare_files(self):
        self._tmp = tempfile.mkdtemp()
        self._trace_file = os.path.join(self._tmp, 'trace')
        self._target_stdout_file = os.path.join(self._tmp, 'stdout')
        self._target_stderr_file = os.path.join(self._tmp, 'stderr')

    def pid(self):
        return self._pid

    def created(self):
        self._process != None

    def terminate(self):
        if self._process:
            self._process.terminate()

    def kill(self):
        if self._process:
            self._process.kill()

    def execute(self, path, args=[]):
        """Executes and traces an executable.
        @param path: path to the executable.
        @param args: args to pass to the executable.
        @return: process object
        """
        self.prepare_files()

        cli = [path] + args
        command = '%s' % ' '.join(cli)

        # TODO: save the target program's standard output and standard error
        cmd = [
            'sudo',
            '/usr/sbin/dtrace',
            '-s',
            self.d_script,
            '-o', self._trace_file,
            '-c', command
        ]

        with open(self._target_stdout_file, 'w') as out:
            with open(self._target_stderr_file, 'w') as err:
                self._process = subprocess.Popen(
                    cmd,
                    stdout=out,
                    stderr=err,
                    bufsize=1)

        # TODO(phretor): do introspection to get the PID of the traced proc
        self._pid = self._process.pid
