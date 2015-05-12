# Copyright (C) 2014 Federico (phretor) Maggi

import re
import logging

from parsers.base import ResultParser

logger = logging.getLogger(__name__)

TYPE_MAPPING = {
    'U': 'undefined',
    'A': 'absolute',
    'T': 'text',
    'D': 'data',
    'B': 'bss',
    'C': 'common',
    'I': 'indirect',
    'S': 'other',

    '-': 'debugging',

    'u': 'undefined',
    'a': 'absolute',
    't': 'text',
    'd': 'data',
    'b': 'bss',
    'c': 'common',
    'i': 'indirect',
    's': 'other'
}

class SymbolsParser(ResultParser):
    def __init__(self, *args, **kwargs):
        if 'type_mapping' in kwargs:
            self.type_mapping = kwargs.get('type_mapping')
        else:
            self.type_mapping = TYPE_MAPPING

    def parse(self, stream, *args, **kwargs):
        symbols = {
            'undefined': [],
            'absolute': [],
            'text': [],
            'data': [],
            'bss': [],
            'common': [],
            'indirect': [],
            'other': [],
            'debugging': [],
        }

        splitter = re.compile('[\s\t]+')

        for row in stream:
            row = row.strip()
            parts = splitter.split(row)

            o, t, n = -1, 0, 0

            if len(parts) == 3:
                o, t, n = parts
            elif len(parts) == 2:
                t, n = parts

            logger.debug('Parsing line: %s', parts)

            line = {'offset': o, 'name': n}

            try:
                symbols[self.type_mapping[t]].append(line)
            except KeyError:
                symbols['other'].append(line)

        return symbols
