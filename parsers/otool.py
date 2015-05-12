# Copyright (C) 2014 Federico (phretor) Maggi

from parsers.base import ResultParser

class OtoolParser(ResultParser):
    def library_parser(self, row):
        path, version = row.split(' (')
        version = version.replace(')', '')
        return path, version

    def parse(self, iterable, *args, **kwargs):
        libraries = []

        for i, row in enumerate(iterable):
            print i, row

            if i > 0:
                row = row.strip()

                if len(row) > 0:
                    path, version = self.library_parser(row)

                    if version is not None:
                        libraries.append({'path': path, 'version': version})
                    else:
                        libraries.append({'path': path})

        return libraries

otool_parser = lambda x: OtoolParser()(x)

def main():
    import sys
    with open(sys.argv[1]) as stream:
        import pprint; pprint.pprint(otool_parser(stream))

if __name__ == '__main__':
    main()
