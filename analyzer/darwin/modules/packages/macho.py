from lib.common.abstracts import Package
from lib.api.process import Process
from lib.common.exceptions import CuckooPackageError

class MachO(Package):
    """MachO analysis.package."""

    def _bundle(self, path):
        """
        Create a Bundle.app from a single MachO file.
        """
        return path

    def start(self, path):
        bundle_path = self._bundle(path)
        args = self.options.get('arguments')
        return self.execute(bundle_path, args)

    def check():
        return True

    def finish():
        return True
