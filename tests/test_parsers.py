import os
import glob
import unittest

from parsers import Parser
from parsers import PARSERS_CONFIG
from utils.loading import load_by_name

class BaseTestParsers(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.dumps = 'dumps'
        self.dumps_dir = os.path.join(self.base_dir, self.dumps)
        self.files = glob.glob(os.path.join(self.dumps_dir, '.*')) + \
                     glob.glob(os.path.join(self.dumps_dir, '*.*'))


class TestParsers(BaseTestParsers):
    def test_init(self):
        p = Parser()

        self.assertTrue(p.ext == None)
        self.assertTrue(p.res == {})
        self.assertTrue(p.config == PARSERS_CONFIG)

    def test_get_parser(self):
        p = Parser()

        fun = p.get_parser()

        self.assertTrue(fun == None)

        for ext, klass in PARSERS_CONFIG.iteritems():
            p = Parser()
            p.ext = ext
            fun = p.get_parser()
            self.assertTrue(fun != None)
            fun_class = load_by_name(klass)
            self.assertTrue(isinstance(fun, fun_class))

    def test_parse(self):
        for f in self.files:
            p = Parser()
            res = p.parse(f, None, False)

            self.assertTrue(
                isinstance(res, dict) or \
                isinstance(res, list) or \
                res is None)

            res = p.parse(f, None, True)

            self.assertTrue(isinstance(res, tuple))
            self.assertTrue(len(res) == 2)

            res = p.parse(f, None, False)

            def_parser = PARSERS_CONFIG.get(p.ext, None)

            cond = def_parser != None and res != {} or\
                   def_parser == None and res == {}

            self.assertTrue(cond)


class BaseTestFileParser(BaseTestParsers):
    filename = ''

    def setUp(self):
        super(BaseTestFileParser, self).setUp()

        self.f = os.path.join(self.dumps_dir, self.filename)


class TestFsloggerParser(BaseTestFileParser):
    filename = '.fslogger'

    def test_main(self):
        p = Parser()
        res = p.parse(self.f, None, False)

        self.assertTrue(len(res) == 9)

    def test_pid(self):
        p = Parser()
        res = p.parse(self.f, None, False)

        for pid, trace in res.iteritems():
            for timestamp, data in trace.iteritems():
                self.assertTrue(pid == data['pid'])
                self.assertTrue(timestamp == data['timestamp'])

                for item in ('path', 'timestamp', 'type'):
                    self.assertTrue(item in data)


class TestSymbolsParser(BaseTestFileParser):
    filename = '.nm'

    def test_main(self):
        p = Parser()
        res = p.parse(self.f, None, False)

        self.assertTrue(len(res) == 9)

        for grp, data in res.iteritems():
            self.assertTrue(isinstance(data, list))

            for symbol in data:
                self.assertTrue(isinstance(symbol, dict))
                self.assertTrue(isinstance(symbol['name'], basestring))
                self.assertTrue(
                    isinstance(symbol['offset'], basestring) or \
                    isinstance(symbol['offset'], int))


class TestOtoolParser(BaseTestFileParser):
    filename = '.otool'

    def test_main(self):
        p = Parser()

        res = p.parse(self.f, None, False)

        self.assertTrue(len(res) == 6)

        for e in res:
            self.assertTrue(isinstance(e, dict))
            self.assertTrue(isinstance(e['path'], basestring))
            self.assertTrue(isinstance(e['version'], basestring))


class TestDtrussParser(BaseTestFileParser):
    filename = '.dtruss'

    def test_summary(self):
        p = Parser()
        res = p.parse(self.f, None, False)

        self.assertTrue(res['summary'] is not None)
        self.assertTrue(len(res['summary']) == 46)

    def test_trace(self):
        p = Parser()
        res = p.parse(self.f, None, False)

        self.assertTrue(res['trace'] is not None)
        self.assertTrue(len(res['trace']) == 268)


if __name__ == '__main__':
    unittest.main()
