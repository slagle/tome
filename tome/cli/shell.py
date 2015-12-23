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
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class TomeApp(App):

    def __init__(self):
        super(TomeApp, self).__init__(
            description='tome app',
            version='0.1',
            command_manager=CommandManager('tome.cli.commands'),
            )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.info('################################################')
        self.LOG.info('# Starting run of tome...')
        self.LOG.info('################################################')
        self.LOG.info('')
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

    def build_option_parser(self, *args, **kwargs):
        parser = super(TomeApp, self).build_option_parser(*args, **kwargs)
        return parser

    def configure_logging(self):
        if self.options.debug:
            logging.basicConfig(level=logging.DEBUG)
        super(TomeApp, self).configure_logging()

def main(argv=sys.argv[1:]):
    tome_app = TomeApp()
    tome_app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
