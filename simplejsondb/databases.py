import typing

import os
import json
import atexit


class Database:

    def __init__(self,
                 path: str,
                 default: typing.Any = None,
                 overwrite: bool = False,
                 save_at_exit: bool = True,
                 ):
        self.path = path

        if not os.path.isfile(self.path) or overwrite:
            self.data = default

        else:
            self.load()

        if save_at_exit:
            atexit.register(self.save)

    @property
    def folder(self,) -> str:
        return os.path.abspath(os.path.dirname(self.path))

    def load(self,) -> None:
        with open(self.path, 'r') as file:
            self.data = json.load(file)

    def save(self, **additional) -> None:
        os.makedirs(self.folder, exist_ok=True)

        with open(self.path, 'w') as file:
            json.dump(self.data, file, **additional)
