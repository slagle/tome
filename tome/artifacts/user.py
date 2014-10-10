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

    def realize(self):
        execute("useradd", self.username)

    def unrealize(self):
        execute("userdel", self.username)

    @classmethod
    def is_realized(cls, username=None):
        if username is None:
            username = cls.username
        try:
            entry = pwd.getpwnam(username)
        except KeyError, e:
            return False
        return True
