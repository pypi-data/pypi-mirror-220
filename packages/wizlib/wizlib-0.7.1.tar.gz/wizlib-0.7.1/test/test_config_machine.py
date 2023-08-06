from unittest import TestCase
from argparse import ArgumentParser
import os
from unittest.mock import patch
from pathlib import Path

from wizlib.config_machine import ConfigMachine


class TestConfig(TestCase):

    def test_direct_arg(self):
        p = ArgumentParser()
        p.add_argument('--foo')
        a = p.parse_args(['--foo', 'bar'])
        config = ConfigMachine('myapp', a)
        f = config.get('foo')
        self.assertEqual(f, 'bar')

    def test_config_file_arg(self):
        p = ArgumentParser()
        p.add_argument('--config')
        a = p.parse_args(
            ['--config', 'test/data_config_machine/test-config.yml'])
        config = ConfigMachine('myapp', a)
        f = config.get('foo')
        self.assertEqual(f, 'erg')

    def test_nested_entry(self):
        p = ArgumentParser()
        p.add_argument('--config')
        a = p.parse_args(
            ['--config', 'test/data_config_machine/test-config.yml'])
        config = ConfigMachine('myapp', a)
        f = config.get('bar-zing')
        self.assertEqual(f, 'ech')

    def test_nested_entry_fail(self):
        p = ArgumentParser()
        p.add_argument('--config')
        a = p.parse_args(
            ['--config', 'test/data_config_machine/test-config.yml'])
        config = ConfigMachine('myapp', a)
        f = config.get('bar-za')
        self.assertIsNone(f)

    def test_specific_env_var(self):
        os.environ['DEF_G'] = 'ju'
        config = ConfigMachine('myapp')
        f = config.get('def-g')
        del os.environ['DEF_G']
        self.assertEqual(f, 'ju')

    def test_specific_env_var(self):
        os.environ['MYAPP_CONFIG'] = 'test/data_config_machine/test-config.yml'
        config = ConfigMachine('myapp')
        f = config.get('bar-zing')
        del os.environ['MYAPP_CONFIG']
        self.assertEqual(f, 'ech')

    def test_local_config_file(self):
        with patch('pathlib.Path.cwd',
                   lambda: Path('test/data_config_machine')):
            config = ConfigMachine('myapp')
            f = config.get('bar-zing')
        self.assertEqual(f, 'ech')

    def test_home_config_file(self):
        with patch('pathlib.Path.home',
                   lambda: Path('test/data_config_machine')):
            config = ConfigMachine('myapp')
            f = config.get('bar-zing')
        self.assertEqual(f, 'ech')
