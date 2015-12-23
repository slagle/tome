#!/usr/bin/env python
#
# Copyright 2015 James Slagle <james.slagle@gmail.com>
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
from types import *
import urllib2

from tome.artifact import Artifact

class File(Artifact):

    path = StringType
    contents = StringType

    __slots__ = [
        'path',
        'contents'
    ]

    def create(self):
        open(self.path, 'w').write(self.contents)

    def delete(self):
        os.unlink(self.path)

    def exists(self, path=None):
        if path is None:
            path = self.path
        return os.path.exists(path)

class HttpFile(File):

    def create(self):
        f = urllib2.urlopen(self.contents)
        open(self.path, 'w').write(f.read())
