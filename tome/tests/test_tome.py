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
from tome.artifacts import package
from tome.cli import commands
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

    def test_delete(self):
        f = TestFile()
        f.delete()
        self.assertFalse(os.path.exists(TestFile.path))

    def test_create(self):
        f = TestFile()
        f.delete()
        self.assertFalse(os.path.exists(TestFile.path))
        f.create()
        self.assertTrue(os.path.exists(TestFile.path))
        self.assertEquals(open(TestFile.path).read(), TestFile.contents)

    def test_exists(self):
        f = TestFile
        self.assertFalse(f.exists())
        f = f()
        self.assertTrue(f.exists())
        f.delete()
        self.assertFalse(f.exists())

    def test_cls_exists(self):
        self.assertFalse(TestFile.exists())
        TestFile()
        self.assertTrue(TestFile.exists())

    def test_cls_create(self):
        self.assertFalse(TestFile.exists())
        TestFile.create()
        self.assertTrue(TestFile.exists())

    def test_cls_delete(self):
        self.assertFalse(TestFile.exists())
        TestFile.create()
        self.assertTrue(TestFile.exists())
        TestFile.delete()
        self.assertFalse(TestFile.exists())

class TestArtifact(base.TestCase):
    pass


class TestArtifactCommand(base.TestCase):

    def setUp(self):
        super(TestArtifactCommand, self).setUp()
        self.ac = commands.ArtifactCommand(None, None)
        self.artifact_file = ''
        self.artifact_path = ''

    def tearDown(self):
        super(TestArtifactCommand, self).tearDown()
        if self.artifact_path:
            os.unlink(self.artifact_path)

    def test_normalize_module_name(self):
        ac = commands.ArtifactCommand(None, None)
        self.assertEquals('testfoo',
            ac.normalize_module_name('testfoo.py')[1])
        self.assertEquals('testbar.testfoo',
            ac.normalize_module_name('testbar.testfoo.py')[1])
        self.assertEquals('/path/to/module',
            ac.normalize_module_name('/path/to/module/testbar.testfoo.py')[0])

    def setup_artifact(self):
        self.artifact_file, self.artifact_path = \
            tempfile.mkstemp(suffix='.py')

        os.write(self.artifact_file, """
from tome.artifacts.package import YumPackage

class Foo(YumPackage):
    name = 'foo'
""")

    def test_get_module_artifacts(self):
        self.setup_artifact()
        module_path, module_name = self.ac.normalize_module_name(self.artifact_path)
        artifacts = self.ac.get_module_artifacts(module_path, module_name)
        self.assertEquals(len(artifacts), 1)
        self.assertTrue(issubclass(artifacts[0], package.YumPackage))
