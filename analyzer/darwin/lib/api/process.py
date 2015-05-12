# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import logging
import multiprocessing

from lib.common.constants import PATHS
from lib.api.tracer import DTrace

log = logging.getLogger(__name__)

class Process(object):
    """Mac OS X process."""

    def execute(self, path, args=None):
        """Execute and trace sample process.
        @param path: sample path.
        @param args: process args.
        @return: operation status.
        """

        tracer = DTrace()
        tracer.execute(path, args)

        created = tracer.created()

        if created:
            # TODO(phretor): set PID
            self.pid = tracer.pid()
            log.info("Successfully executed process from path \"%s\" with "
                     "arguments \"%s\" with pid %d", path, args or "", self.pid)
            return True
        else:
            log.error("Failed to execute process from path \"%s\" with "
                      "arguments \"%s\"", path, args)
            return False

    def terminate(self):
        """Terminate process.
        @return: operation status.
        """
        pass
