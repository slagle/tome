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


import logging
import runpy
import sys
import types

from cliff.command import Command

from tome.artifact import Artifact, ArtifactMeta
from tome.artifacts import *


class ArtifactCommand(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ArtifactCommand, self).get_parser(prog_name)
        parser.add_argument('artifact', action='store', nargs='+',
            help='Artifact to add')
        return parser

    def normalize_module_name(self, artifact):
        self.log.debug('Looking for artifact: %s' % artifact)
        module_path = '/'.join(artifact.split('/', -1)[0:-1])
        module_name = artifact.split('/', -1)[-1]
        if module_name.endswith('.py'):
            self.log.debug('stripping .py from artifact name')
            module_name = module_name.strip('.py')
        return module_path, module_name

    def get_module_artifacts(self, module_path, module_name):
        self.log.debug('attempting import of %s' % module_name)
        sys.path.insert(0, module_path)
        module_dict = runpy.run_module(module_name)
        artifacts = []
        for k, v in module_dict.items():
            if hasattr(v, '__module__'):
                if v.__module__ == module_name:
                    if type(v) == ArtifactMeta:
                        artifacts.append(v)
        return artifacts

    def get_artifacts(self, artifact):
        self.log.debug('loading artifact %s' % artifact)
        module_path, module_name = self.normalize_module_name(artifact)
        artifacts = self.get_module_artifacts(module_path, module_name)
        return artifacts

    def take_action(self, parsed_args):
        raise NotImplementedError


class Create(ArtifactCommand):
    "Create an atrifact"

    def take_action(self, parsed_args):
        self.log.info('# Running Create Command')
        for artifact in parsed_args.artifact:
            artifacts = self.get_artifacts(artifact)
            for _artifact in artifacts:
                self.log.info('## Creating %s from %s' \
                        % (_artifact.__name__, artifact))
                self.log.debug('instantiating %s' % _artifact)
                _artifact()


class Delete(ArtifactCommand):
    "Delete an atrifact"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('# Running Remove Command')
        for artifact in parsed_args.artifact:
            artifacts = self.get_artifacts(artifact)
            for _artifact in artifacts:
                if _artifact.exists():
                    self.log.info('Deleting %s from %s' \
                            % (_artifact.__name__, artifact))
                    self.log.debug('deleting %s' % _artifact)
                    _artifact.delete()
                else:
                    self.log.info('%s from %s does not exist, not deleting' \
                            % (_artifact.__name__, artifact))


class Exists(ArtifactCommand):
    "Test if an artifact exists"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('# Running Exists Command')
        for artifact in parsed_args.artifact:
            artifacts = self.get_artifacts(artifact)
            for _artifact in artifacts:
                if _artifact.exists():
                    self.log.info('-- %s from %s exists' \
                            % (_artifact.__name__, artifact))
                else:
                    self.log.info('-- %s from %s doesn\'t exist' \
                            % (_artifact.__name__, artifact))
