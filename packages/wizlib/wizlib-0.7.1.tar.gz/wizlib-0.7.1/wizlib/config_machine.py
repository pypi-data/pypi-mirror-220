from dataclasses import dataclass
from argparse import Namespace
from pathlib import Path
import os

from yaml import load
from yaml import Loader


@dataclass
class ConfigMachine:
    """
    Attributes:

    appname - The name of the config file, environment variable, etc.
    args - an argparse namespace object
    """

    appname: str
    args: Namespace = None

    @property
    def yaml(self):
        if hasattr(self, '_yaml'):
            return self._yaml
        if hasattr(self.args, 'config'):
            path = Path(self.args.config)
        elif (envvar := self.env(self.appname + '-config')):
            path = Path(envvar)
        elif ((localpath := Path.cwd() / f".{self.appname}.yml").is_file()):
            path = localpath
        elif ((homepath := Path.home() / f".{self.appname}.yml").is_file()):
            path = homepath
        else:
            path = None
        if path:
            with open(path) as file:
                self._yaml = load(file, Loader=Loader)
                return self._yaml

    @staticmethod
    def env(name):
        if (envvar := name.upper().replace('-', '_')) in os.environ:
            return os.environ[envvar]

    def get(self, key: str):
        if hasattr(self.args, key):
            return getattr(self.args, key)
        if (result := self.env(key)):
            return result
        if (yaml := self.yaml):
            split = key.split('-')
            while (val := split.pop(0)) and (val in yaml):
                yaml = yaml[val] if val in yaml else None
                if not split:
                    return yaml
