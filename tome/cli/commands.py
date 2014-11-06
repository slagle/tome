import logging
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

    def module_name(self, artifact):
        self.log.debug('Looking for artifact: %s' % artifact)
        if artifact.endswith('.py'):
            self.log.debug('stripping .py from artifact name')
            module_name = artifact.strip('.py')
        else:
            module_name = artifact
        return module_name

    def module_object(self, module_name):
        self.log.debug('attempting import of %s' % module_name)
        module = __import__(module_name)
        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if type(obj) == ArtifactMeta:
                if not obj.do_commands:
                    continue
                return obj

    def artifact_class(self, artifact):
        self.log.debug('loading artifact %s' % artifact)
        module_name = self.module_name(artifact)
        module_object = self.module_object(module_name)
        return module_object


class Add(ArtifactCommand):
    "Add an atrifact"

    def take_action(self, parsed_args):
        for artifact in parsed_args.artifact:
            obj = self.artifact_class(artifact)
            self.log.debug('instantiating %s' % obj)
            obj()

        self.log.info('add complete')

class Remove(ArtifactCommand):
    "Remove an atrifact"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        for artifact in parsed_args.artifact:
            obj = self.artifact_class(artifact)
            if obj._exists():
                self.log.debug('removing %s' % obj)
                obj._remove()
            else:
                self.log.info('%s does not exist, not removing' % obj)

        self.log.info('remove complete')

class Exists(ArtifactCommand):
    "Test if an artifact exists"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        for artifact in parsed_args.artifact:
            obj = self.artifact_class(artifact)
            if obj._exists():
                self.log.info('%s exists' % artifact)
            else:
                self.log.info('%s doesn''t exist' % artifact)
