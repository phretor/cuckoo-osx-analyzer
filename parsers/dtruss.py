# Copyright (C) 2014 Federico (phretor) Maggi

import re
import logging

OPT_SPACES = "[\s\t]*"
SPACES = "[\s\t]+"
SLASH = "\/"
COLON = "\:"
OPENP = "\("
CLOSEP = "\)"
EQUALS = "\="
BACKTICK = "\`"

from parsers.base import ResultParser

logger = logging.getLogger(__name__)

class DtrussParser(ResultParser):
    st_re = re.compile(
        "^" +
        OPT_SPACES +
        "(?P<binary>[^`]+)" +
        BACKTICK +
        "(?P<fun_name>[^(]+)" +
        "(\((?P<arg_list>[^)]+)\))?" +
        "[+]?" +
        "(?P<offset>[^$]+)" +
        "$"
    )

    call_re = re.compile(
        "^" +
        "(?P<pid>[0-9]+)" +
        SLASH +
        "(?P<thread>[^:]+)" +
        COLON +
        SPACES +
        "(?P<relative_time>[0-9]+)" +
        SPACES +
        "(?P<elapsed_time>[0-9]+)" +
        SPACES +
        "(?P<cpu_time>[0-9]+)" +
        SPACES +
        "(?P<syscall>[^(]+)" +
        OPENP +
        "(?P<args>[^)]+)" +
        CLOSEP +
        SPACES +
        EQUALS +
        SPACES +
        "(?P<retval>[-]?[0-9]+)" +
        OPT_SPACES +
        "(?P<retvalg>(?P<err>Err\#)?(?P<retval2>[0-9]+))" +
        "$"
    )

    def parse_call(self, matches):
        m = matches.groupdict()

        if isinstance(m['args'], basestring):
            m['args'] = m['args'].split(', ')

        if m['err']:
            m['err'] = True
        else:
            m['err'] = False

        return m

    def parse_stacktrace_row(self, matches):
        m = matches.groupdict()
        if isinstance(m['arg_list'], basestring):
            m['arg_list'] = m['arg_list'].split(', ')
        return m

    def parse_count(self, row):
        row = re.sub("[\s\t]{2,}", ' ', row)
        call, count = row.split(' ')
        return {
            'syscall': call,
            'count': count
        }

    def parse(self, stream, *args, **kwargs):
        trace = []
        summary = None
        call = {}

        for f in stream:
            logger.debug('Parsing DTruss line: %s', f)

            f = f.strip()

            if len(f) > 0:
                if f.startswith('CALL'):     # summary beginning?
                    summary = []
                elif summary is not None:    # summary line?
                    summary.append(self.parse_count(f))
                else:                        # something else?
                    call_m = self.call_re.match(f)

                    if call_m:               # call?
                        if call != {}:
                            trace.append(call)
                        call = {
                            'call': self.parse_call(call_m)
                        }
                    elif not f.startswith('PID/THRD'):  # something else?
                        st_m = self.st_re.match(f)
                        if st_m:             # stacktrace?
                            parsed_st = self.parse_stacktrace_row(st_m)
                            if 'stacktrace' in call:
                                call['stacktrace'].append(parsed_st)
                            else:
                                call['stacktrace'] = [parsed_st]

        res = {
            'trace': trace,
            'summary': summary
        }

        logger.debug('Returning %s', res)

        return res

trace_parser = lambda x: DtrussParser()(x)

def main():
    import sys
    import pprint
    with open(sys.argv[1]) as stream:
        import pprint; pprint.pprint(trace_parser(stream))

if __name__ == '__main__':
    main()
