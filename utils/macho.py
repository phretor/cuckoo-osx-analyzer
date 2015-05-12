# Copyright (C) 2014 Federico (phretor) Maggi

import os
import random
import shutil
import string
import logging
import tempfile

from . import make_zipfile

logger = logging.getLogger(__name__)

INFO_PLIST_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
%(dict)s
</dict>
</plist>'''

INFO_PLIST_DICT = {
    'CFBundleDevelopmentRegion': 'English',
    'CFBundleExecutable': 'Bundle',
    'CFBundleGetInfoString': 'Bundle',
    'CFBundleIconFile': 'app.icns',
    'CFBundleIdentifier': 'it.machobox.Bundle', # TODO (phretor): change this :)
    'CFBundleInfoDictionaryVersion': '1.0',
    'CFBundleName': 'Bundle',
    'CFBundlePackageType': 'APPL',
    'CFBundleShortVersionString': '1.0',
    'CFBundleSignature': 'myap',
    'CFBundleVersion': '1.0.0',
    'NSAppleScriptEnabled': 'YES',
    'NSMainNibFile': 'MainMenu',
    'NSPrincipalClass': 'NSApplication'}

BUNDLE_STRUCTURE = [
    'Contents/MacOS',
    'Contents/Frameworks',
    'Resources',
    'Support Files'
]

class BundleWrapper(object):
    """A class to prepare a sample as an analysis bundle.
    """
    def __init__(self, info_plist_template=INFO_PLIST_TEMPLATE,
                 info_plist_dict=INFO_PLIST_DICT,
                 bundle_structure=BUNDLE_STRUCTURE, *args, **kwargs):
        self.info_plist_template = info_plist_template
        self.info_plist_dict = info_plist_dict
        self.bundle_structure = bundle_structure

        logger.debug('Creating new bundle')

        executable_name = self.random_executable_name()
        prefix = self.random_prefix()
        identifier = '.'.join(
            (prefix, executable_name))
        signature = self.random_signature()

        update = {
            'CFBundleExecutable': executable_name,
            'CFBundleGetInfoString': executable_name,
            'CFBundleIdentifier': identifier,
            'CFBundleName': executable_name,
            'CFBundleSignature': signature
        }

        self.info_plist_dict.update(update)

        self.executable_name = executable_name
        self.bundle_name = '%s.app' % self.executable_name
        self.zip_name = '%s.zip' % self.bundle_name
        self.executable_relative_path = os.path.join(
            'Contents/MacOS/',
            self.executable_name)

    def random_signature(self):
        return ''.join(random.sample(string.lowercase, 4))

    def render_info_plist(self):
        content = ''
        for k,s in self.info_plist_dict.iteritems():
            content += '<key>%s</key>\n' % k
            content += '<string>%s</string>\n' % s
        return self.info_plist_template % {'dict': content}

    def write_info_plist(self, stream):
        stream.write(self.render_info_plist())

    def random_executable_name(self):
        name = []
        l = random.randint(5, 10)
        name.extend(random.sample(string.uppercase, 1))
        name.extend(random.sample(string.lowercase, l))
        return ''.join(name)

    def random_prefix(self):
        name = []
        for i in xrange(0, random.randint(1, 4)):
            name.extend(random.sample(string.lowercase, random.randint(1, 10)))
            name.append('.')
        return '%s.%s' % (
            ''.join(random.sample(string.lowercase, random.randint(1, 3))),
            ''.join(name))

    def make_structure(self, base, placeholder=True):
        for path in self.bundle_structure:
            d = os.path.join(base, self.bundle_name, path)

            if placeholder:
                f = os.path.join(d, '.' + self.random_prefix())
            os.makedirs(d)

            if placeholder:
                with open(f, 'wb') as touch:
                    touch.write(str(random.randint(0,10)))
            logger.debug('Structure for %s created', path)

    @classmethod
    def create_from_macho(cls, stream_or_path, cleanup=True, in_memory=True):
        this = cls()

        # make dir for zip file
        zip_path = tempfile.mkdtemp()
        logger.debug('Working on temp dir: %s', zip_path)

        zip_base = os.path.join(zip_path, this.bundle_name)
        logger.debug('Zip base path at %s', zip_base)

        # make skel
        base = tempfile.mkdtemp()
        this.make_structure(base)
        bundle_root = os.path.join(base, this.bundle_name)
        this.executable_path = os.path.join(
            bundle_root,
            this.executable_relative_path)

        logger.debug('Skeleton done. Executable path at %s', this.executable_path)

        # write the info file
        info_file_path = os.path.join(bundle_root, 'Contents', 'Info.plist')
        with open(info_file_path, 'w') as fh:
            this.write_info_plist(fh)

        logger.debug('Info file written')

        # copy executable into bundle
        if isinstance(stream_or_path, basestring):
            if os.path.isfile(stream_or_path):
                shutil.copy(stream_or_path, this.executable_path)
                logger.debug('Executable copied into bundle')
        else:
            stream = stream_or_path
            try:
                with open(this.executable_path, 'wb') as fh:
                    stream.seek(0)
                    shutil.copyfileobj(stream, fh)
                    logger.debug('Stream copied into bundle')
            except IOError, e:
                logger.error('Cannot write executable to %s: %s',
                             this.executable_path, e)

        # make zip file
        this.zip_path = make_zipfile(
            zip_base, base, start=base, in_memory=in_memory)

        # cleanup base dir
        if cleanup:
            try:
                shutil.rmtree(base, ignore_errors=True)
            except Exception, e:
                logger.warning('Could not clean up directory: %s', e)
            logger.debug('Directory %s cleaned up', base)

        this.executable_path = os.path.join(
            this.bundle_name, this.executable_relative_path)

        logger.debug('Updating bundle executable path: %s', this.executable_path)

        return this

    def to_dict(self):
        return {
            'zip_name': self.zip_name,
            'zip_path': self.zip_path,
            'bundle_name': self.bundle_name,
            'executable_name': self.executable_name,
            'executable_path': self.executable_path,
            'executable_relative_path': self.executable_relative_path
        }

    def __unicode__(self):
        return u'<BundleWrapper %s>' % self.to_dict()

    def __repr__(self):
        return self.__unicode__()

    @classmethod
    def create_from_zipbundle(cls, stream_or_path):
        #TODO implement this
        pass


    def run(self, **kwargs):
        self.infile = kwargs['infile']
        self.outdir = kwargs['outdir']

        self.main()

    def main(self):
        import os

        bundle = BundleWrapper.create_from_macho(
            self.infile, cleanup=True, in_memory=False)

        shutil.move(bundle.zip_path, self.outdir)

        print os.path.join(self.outdir, bundle.zip_name)

def test():
    import sys
    import zipfile
    from machobox.analyzers.file import Hashes
    from cStringIO import StringIO

    path = sys.argv[1]
    with open(path, 'rb') as stream:
        hashes = Hashes(stream)

        for inm in (True, False):
            bundle = BundleWrapper.create_from_macho(path, in_memory=inm)

            if not inm:
                with zipfile.ZipFile(bundle.zip_path, 'r') as zf:
                    macho = StringIO(zf.read(bundle.executable_path))
            else:
                macho = StringIO(bundle.zip_path.read(bundle.executable_path))

            hashes2 = Hashes(macho)

            assert hashes.sha256 == hashes2.sha256

if __name__ == '__main__':
    test()
