# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_tome
----------------------------------

Tests for `tome` module.
"""

import os
import tempfile

from tome import artifact
from tome.artifacts import file as file_module
from tome.tests import base


class TestFile(file_module.File):
    path = tempfile.mktemp()
    contents = "testcontents"

class TestFileArtifact(base.TestCase):

    def setUp(self):
        self.delete_test_file()
        super(TestFileArtifact, self).setUp()

    def tearDown(self):
        self.delete_test_file()
        super(TestFileArtifact, self).tearDown()

    def delete_test_file(self):
        if os.path.exists(TestFile.path):
            os.unlink(TestFile.path)

    def test_init(self):
        f = TestFile()
        self.assertTrue(os.path.exists(TestFile.path))
        self.assertEquals(open(TestFile.path).read(), TestFile.contents)

    def test_remove(self):
        f = TestFile()
        f.remove()
        self.assertFalse(os.path.exists(TestFile.path))

    def test_add(self):
        f = TestFile()
        f.remove()
        self.assertFalse(os.path.exists(TestFile.path))
        f.add()
        self.assertTrue(os.path.exists(TestFile.path))
        self.assertEquals(open(TestFile.path).read(), TestFile.contents)

    def test_exists(self):
        self.assertFalse(TestFile.exists())
        TestFile()
        self.assertTrue(TestFile.exists())


class TestTome(base.TestCase):

    def test_something(self):
        pass
