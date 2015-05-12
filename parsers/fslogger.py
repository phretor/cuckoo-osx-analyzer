# Copyright (C) 2014 Federico (phretor) Maggi

import re
import logging

from parsers.base import ResultParser

logger = logging.getLogger(__name__)

class FsloggerParser(ResultParser):
    def parse_pid(self, row):
        try:
            return re.findall('[0-9]+', row)[0]
        except:
            pass

    def parse_type(self, row):
        return row.split('= ')[1].strip()

    def parse_string_arg(self, row):
        return row.split(' = ')[1]

    def parse_bytes(self, row):
        try:
            return re.findall('[0-9]+', row.split('=> received ')[1])[0]
        except:
            pass

    def parse_timestamp(self, row):
        return re.findall('[0-9]+', row.split(' = ')[1])[0]

    def parse(self, stream, *args, **kwargs):
        logger.debug('Parsing stream %s', stream)

        event = None
        events = {}     # by pid

        for row in stream:
            logger.debug('Parsing FSlogger line: %s', row)

            if len(row) > 0:
                # start parsing event
                if '# Event' in row:
                    event = {
                        'path': [],
                        'pid': None,
                        'type': None }

                elif isinstance(event, dict):
                    if ' pid ' in row:
                        event['pid'] = self.parse_pid(row)
                    elif ' type ' in row and '= FSE_' in row:
                        event['type'] = self.parse_type(row)
                    elif ' FSE_ARG_STRING ' in row:
                        event['path'].append(self.parse_string_arg(row).strip())
                    elif 'tstamp =' in row:
                        event['timestamp'] = self.parse_timestamp(row)

                if event is not None and 'timestamp' in event:
                    if event['pid'] not in events:
                        events[event['pid']] = {}
                    events[event['pid']][event['timestamp']] = event

        logger.debug('Returning %s', events)
        return events

fslogger_parser = lambda x: FsloggerParser()(x)

def main():
    import sys
    with open(sys.argv[1]) as stream:
        import pprint; pprint.pprint(fslogger_parser(stream))

if __name__ == '__main__':
    main()
