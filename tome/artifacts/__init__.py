import sys

from tome.artifact import ArtifactMeta

from tome.artifacts.file import *
from tome.artifacts.package import *

for obj_name in dir():
    obj = getattr(sys.modules['tome.artifacts'], obj_name)
    if type(obj) == ArtifactMeta:
        obj.do_commands = False
