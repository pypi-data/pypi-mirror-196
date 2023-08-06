import os
from argparse import Namespace

PREFIX = chr(2)


class BaseCommand:
    def __init__(self, options: Namespace):
        self._prefix = "_pvenv_env"
        self._options = options

    def run(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement run")

    @staticmethod
    def print(*args: str, **kwargs):  # noqa: A003
        if not os.getenv("PVENV_DEBUG"):
            args = tuple(f"{PREFIX}{arg}" for arg in args)
        print(*args, **kwargs)
