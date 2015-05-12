#! /usr/bin/env python

# Copyright (C) 2015 Dmitry Rodionov
# This file is part of my GSoC'15 project for Cuckoo Sandbox:
#    http://www.cuckoosandbox.org
# This software may be modified and distributed under the terms
# of the MIT license. See the LICENSE file for details.

# Edits by Federico (phretor) Maggi

import os
import sys
import logging

log = logging.getLogger(__name__)

class Macalyser:
    """Cuckoo OS X analyzer.
    """

    logger = None
    target = ""
    target_artefacts = []
    config= []
    uses_proc_monitor = False

    def __init__(self):
        # setup logging
        # parse the config
        # figure out what the target is
        self.setup_logging()

    def run(self):
        # package = analysis_package_for_current_target()
        # aux = setup_auxiliary_modules()
        #
        # setup_machine_time(self.config.datetime)
        # results = analysis(package)
        #
        # shutdown_auxiliary_modules(aux)
        # shutdown_spawned_modules(results.procs_still_alive)
        # complete()

    def complete(self):
        # upload_artefacts()
        # cleanup()
        pass

    #
    # Implementation details
    #
    def setup_logging(self):
        global log
        self.logger = log

    def parse_config(self, config_name):
        pass

    def analysis_package_for_current_target(self):
        pass

    def setup_auxiliary_modules(self):
        pass

    def setup_machine_time(self, datetime):
        pass

    def analysis(self, package):
        pass

    def shutdown_auxiliary_modules(self, aux):
        pass

    def shutdown_spawned_processes(self, procs):
        pass

    def upload_artefacts(self):
        pass

    def cleanup(self):
        pass

Analyzer = Macalyser

if __name__ == "__main__":
    success = False
    error = ""

    try:
        # Initialize the main analyzer class.
        analyzer = Analyzer()

        # Run it and wait for the response.
        success = analyzer.run()

    # This is not likely to happen.
    except KeyboardInterrupt:
        error = "Keyboard Interrupt"

    # If the analysis process encountered a critical error, it will raise a
    # CuckooError exception, which will force the termination of the analysis.
    # Notify the agent of the failure. Also catch unexpected exceptions.
    except Exception as e:
        # Store the error.
        error_exc = traceback.format_exc()
        error = str(e)

        # Just to be paranoid.
        if len(log.handlers):
            log.exception(error_exc)
        else:
            sys.stderr.write("{0}\n".format(error_exc))

    # Once the analysis is completed or terminated for any reason, we report
    # back to the agent, notifying that it can report back to the host.
    #finally:
    #    # Establish connection with the agent XMLRPC server.
    #    server = xmlrpclib.Server("http://127.0.0.1:8000")
    #    server.complete(success, error, PATHS["root"])
