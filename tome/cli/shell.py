import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

log = logging.getLogger(__name__)

class TomeApp(App):

    def __init__(self):
        super(TomeApp, self).__init__(
            description='tome app',
            version='0.1',
            command_manager=CommandManager('tome.cli.commands'),
            )

    def initialize_app(self, argv):
        log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            log.debug('got an error: %s', err)

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
