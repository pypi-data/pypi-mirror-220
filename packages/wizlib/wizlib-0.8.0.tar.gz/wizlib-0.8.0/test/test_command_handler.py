from unittest import TestCase

from wizlib.command_handler import CommandHandler
from .data_command import TestCommand


class TestCommandSync(TestCase):

    def test_from_handler(self):
        r, s = CommandHandler(TestCommand).handle(['play'])
        self.assertEqual(r, 'Play!')

    def test_default(self):
        r, s = CommandHandler(TestCommand).handle()
        self.assertEqual(r, 'Play!')

    def test_wrong_command(self):
        h = CommandHandler(TestCommand)
        c = h.get_command(['eat'])
        self.assertIsNone(c)

    def test_handle_wrong_command(self):
        h = CommandHandler(TestCommand)
        r, s = h.handle(['eat'])
        self.assertIsNone(r)

    def test_command_arg(self):
        h = CommandHandler(TestCommand)
        c = h.get_command(['play', '--dd', 't'])
        self.assertEqual(c.dd, 't')

    def test_atriarch_args(self):
        h = CommandHandler(TestCommand)
        c = h.get_command(['--xx', 'y', 'play'])
        self.assertEqual(c.xx, 'y')
