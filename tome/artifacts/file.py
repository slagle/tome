import os
from types import *

from tome.artifact import Artifact

class File(Artifact):

    path = StringType
    contents = StringType

    __slots__ = [
        'path',
        'contents'
    ]

    def add(self):
        open(self.path, 'w').write(self.contents)

    def remove(self):
        os.unlink(self.path)

    @classmethod
    def exists(cls, path=None):
        if path is None:
            path = cls.path
        return os.path.exists(path)
