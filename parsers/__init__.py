# Copyright (C) 2014 Federico (phretor) Maggi

import os

import logging
import pprint

from parsers.dtruss import DtrussParser
from parsers.strings import StringsParser
from parsers.otool import OtoolParser
from parsers.fslogger import FsloggerParser
from parsers.nm import SymbolsParser

from utils.loading import load_by_name

logger = logging.getLogger(__name__)

__all__ = [
    'DtrussParser',
    'StringsParser',
    'OtoolParser',
    'FsloggerParser',
    'SymbolsParser']

PARSERS_CONFIG = {
    #'extension': 'parser.module.ClassName'
    'dtruss':   'parsers.DtrussParser',
    'fslogger': 'parsers.FsloggerParser',
    'nm':       'parsers.SymbolsParser',
    'otool':    'parsers.OtoolParser',
}

class Parser(object):
    def __init__(self, config=None):
        if config is not None:
            self.config = config
        else:
            self.config = PARSERS_CONFIG

        self.ext = None
        self.res = {}

    def get_parser(self):
        fun_name = None
        fun = None

        if self.ext is None:
            return None

        logger.debug('Loading parser for type %s', self.ext)

        if self.ext in self.config:
            fun_name = self.config[self.ext]

        if fun_name is not None:
            fun = load_by_name(fun_name)

        if isinstance(fun, type):
            fun = fun()

        return fun

    def _parse_file(self, path, fun):
        logger.debug('Parsing file with function %s', fun)
        try:
            with open(path) as stream:
                self.res = fun(stream)
        except IOError, e:
            logger.warning('Failed opening %s: %s', path, e)

    def _parse_stream(self, stream, fun):
        logger.debug('Parsing stream with function %s', fun)
        self.res = fun(stream)

    def _return(self, return_type):
        logger.debug('Parsing done. Returning "%s" %s',
                     self.ext,  pprint.pformat(self.res))

        if return_type:
            return (self.ext, self.res)
        else:
            return self.res

    def parse(self, path_or_stream, ext, return_type=False):
        self.res = {}
        stream = False

        if isinstance(path_or_stream, basestring):
            if os.path.isfile(path_or_stream):
                _, filename = os.path.split(path_or_stream)
                _, self.ext = filename.split('.')
                logger.debug('Parsing %s file', ext)
            else:
                return self._return(return_type)
        else:
            self.ext = ext
            stream = True
            logger.debug('Parsing "%s" stream', ext)

        fun = self.get_parser()

        if fun is None:
            logger.warning('Returning early because "fun" for "%s" is none', \
                           self.ext)
            return self._return(return_type)

        if not stream:
            self._parse_file(path=path_or_stream, fun=fun)
        else:
            self._parse_stream(stream=path_or_stream, fun=fun)

        logger.debug('Returning as expected for "%s"', self.ext)

        return self._return(return_type)

    __call__ = parse
