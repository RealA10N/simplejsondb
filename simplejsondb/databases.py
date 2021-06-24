import typing

import os
import json
import atexit


class Database:

    def __init__(self,
                 path: str,
                 default: typing.Any = None,
                 save_at_exit: bool = True,
                 ):
        self.path = path

        if os.path.isfile(self.path):
            self.load()

        else:
            self.data = default

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
