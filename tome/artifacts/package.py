import rpm
from types import *

from tome.artifact import Artifact
from tome.openstack.common import processutils


class Package(Artifact):

    name = StringType
    
    __slots__ = [
        'name',
    ]

class RPMPackage(Package):

    def exists(self):
        ts = rpm.TransactionSet()
        mi = ts.dbMatch('name', 'zsh')
        if mi.count() > 0:
            return True
        else:
            return False

class YumPackage(RPMPackage):
    
    def add(self):
        processutils.execute(
            '/usr/bin/sudo', 'yum', '-y', 'install', self.name)

    def remove(self):
        processutils.execute(
            '/usr/bin/sudo', 'yum', '-y', 'erase', self.name)
        

