import pwd

from tome.artifact import Artifact
from tome.openstack.common.processutils import execute

class User(Artifact):

    username = None
    homedir = None

    __slots__ = [
        "username",
        "homedir"
    ]

    def _realize(self):
        execute("useradd", self.username)

    def _unrealize(self):
        execute("userdel", self.username)

    def _is_realized(self):
        try:
            entry = pwd.getpwnam(self.username)
        except KeyError, e:
            return False
        return True
