# Copyright (C) 2014 Federico (phretor) Maggi

class ResultParser(object):
    def __init__(self, *args, **kwargs):
        super(ResultParser, self).__init__(*args, **kwargs)

    def __call__(self, stream, *args, **kwargs):
        return self.parse(stream, *args, **kwargs)

    def parse(self, stream, *args, **kwargs):
        raise NotImplementedError('Subclasses must implement parse()')
