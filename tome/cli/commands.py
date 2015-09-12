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


class Add(ArtifactCommand):
    "Add an atrifact"

    def take_action(self, parsed_args):
        self.stdout.write('# Running Add Command\n')
        self.stdout.write('\n')
        for artifact in parsed_args.artifact:
            artifacts = self.get_artifacts(artifact)
            for _artifact in artifacts:
                self.log.debug('instantiating %s' % _artifact)
                _artifact()

        self.log.info('add complete')

class Remove(ArtifactCommand):
    "Remove an atrifact"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.stdout.write('# Running Remove Command\n')
        self.stdout.write('\n')
        for artifact in parsed_args.artifact:
            artifacts = self.get_artifacts(artifact)
            for _artifact in artifacts:
                if _artifact.exists():
                    self.log.debug('removing %s' % _artifact)
                    _artifact.remove()
                else:
                    self.log.info('%s does not exist, not removing' %
                                  _artifact)

        self.log.info('remove complete')

class Exists(ArtifactCommand):
    "Test if an artifact exists"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.stdout.write('# Running Exists Command\n')
        self.stdout.write('\n')
        for artifact in parsed_args.artifact:
            artifacts = self.get_artifacts(artifact)
            for _artifact in artifacts:
                if _artifact._exists():
                    self.log.info('%s exists' % _artifact)
                else:
                    self.log.info('%s doesn''t exist' % _artifact)
