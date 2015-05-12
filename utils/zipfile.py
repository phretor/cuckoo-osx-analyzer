# Copyright (C) 2014 Federico (phretor) Maggi
import os
import logging
import zipfile
from cStringIO import StringIO

logger = logging.getLogger(__name__)

class InMemoryZip(zipfile.ZipFile):
    def __init__(self, *args, **kwargs):
        # Create the in-memory file-like object
        self.in_memory_data = StringIO()
        # Create the in-memory zipfile
        zipfile.ZipFile.__init__(self,self.in_memory_data, "w")

    def get_raw(self):
        # no flush for zipfile we need to close, if needed we can reopen the
        # zipfile later...
        zipfile.ZipFile.close(self)
        raw = self.in_memory_data.getvalue()
        return raw

    def get_raw_encoded(self):
        from base64 import b64encode
        return b64encode(self.get_raw())

    def close(self):
        #zipfile already closed if get_raw is called
        #just free the in-memory data file
        self.in_memory_data.close()


def make_zipfile(base_name, base_dir, start=None, in_memory=False):
    """Create a zip file from all the files under 'base_dir'.
    """
    zip_filename = base_name + ".zip"

    logger.debug('Making new Zip file: %s (%s)', zip_filename, base_name)

    def visit (z, dirname, names):
        for name in names:
            path = os.path.normpath(os.path.join(dirname, name))

            # relpath is the path within the ZIP file
            if start is not None:
                relpath = os.path.relpath(path, start)
            else:
                relpath = path
            if os.path.isfile(path):
                z.write(path, relpath)

    if in_memory:
        klass = InMemoryZip
        logger.debug('Making in-memory Zip file')
    else:
        klass = zipfile.ZipFile
        logger.debug('Making regular Zip file')

    z = klass(zip_filename, "w", compression=zipfile.ZIP_DEFLATED)
    os.path.walk(base_dir, visit, z)

    if not in_memory:
        logger.debug('Closing regular Zip file handler')
        z.close()

    if in_memory:
        logger.debug('Returing in-memory Zip file instance')
        return z

    logger.debug('Returing regular Zip file name')
    return zip_filename


def test():
    import sys
    import tempfile
    basename = tempfile.mkdtemp()
    imzf = make_zipfile(
        base_name=os.path.join(basename, 'temp_test'),
        base_dir=sys.argv[1],
        start=basename,
        in_memory=False)
    print imzf


if __name__ == '__main__':
    test()
