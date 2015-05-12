# Copyright (C) 2015 Federico (phretor) Maggi

import os
import fcntl
import logging
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
        self._stdout = None
        self._stderr = None

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

    def execute(self, path, args):
        """Executes and traces an executable.
        @param path: path to the executable.
        @param args: args to pass to the executable.
        @return: process object
        """
        command = '"%s"' % ' '.join([path, args])
        cmd = ['sudo', self.d_script, '-c', command]

        self._process = subprocess.Popen(cmd,
                                         bufsize=1,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

        self._stdout = self._process.stdout
        self._stderr = self._process.stderr

        fcntl.fcntl(self._stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(self._stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

        # TODO(phretor): do introspection to get the PID of the traced proc
        self._pid = self._process.pid
