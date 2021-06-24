import typing
import logging

import os
import json
import atexit

logger = logging.getLogger(__name__)


class DatabaseMeta(type):

    _instances = dict()

    def __call__(cls, path: str, *args, **kwargs):
        path = os.path.abspath(path)

        if path not in cls._instances:
            cls._instances[path] = super(
                DatabaseMeta, cls).__call__(path, *args, **kwargs)

        return cls._instances[path]


class Database(metaclass=DatabaseMeta):

    def __init__(self,
                 path: str,
                 default: typing.Any = None,
                 save_at_exit: bool = True,
                 ):
        self.path = path

        logger.debug('Created Database instance for file %s', self.path)

        if os.path.isfile(self.path):
            self.load()

        else:
            self.data = default
            logger.debug('Loaded default data %s into Database instance for %s',
                         self.data, self.path)

        if save_at_exit:
            atexit.register(self.save)

    @property
    def folder(self,) -> str:
        return os.path.abspath(os.path.dirname(self.path))

    def load(self,) -> None:
        with open(self.path, 'r') as file:
            self.data = json.load(file)

        logger.debug('Loaded data from %s', self.path)

    def save(self, **additional) -> None:
        os.makedirs(self.folder, exist_ok=True)

        with open(self.path, 'w') as file:
            json.dump(self.data, file, **additional)

        logger.debug('Saved data into file %s', self.path)


class DatabaseFolder:

    def __init__(self, folder: str, **options):
        self.folder = folder
        self._options = options

    def _name_to_filepath(self, name: str) -> str:
        return os.path.join(self.folder, f'{name}.json')

    def __getitem__(self, name: str):
        return Database(
            self._name_to_filepath(name),
            **self._options,
        ).data

    def __setitem__(self, name: str, value):
        Database(
            self._name_to_filepath(name),
            **self._options,
        ).data = value

