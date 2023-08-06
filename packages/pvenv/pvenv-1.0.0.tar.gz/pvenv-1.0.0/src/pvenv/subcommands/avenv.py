from __future__ import annotations

import os
from argparse import Namespace
from pathlib import Path
from typing import Any

from dj_settings import SettingsParser

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)
        self.base_dir: Path = options.base_dir
        self.venv: str = options.venv
        self.cd: bool = options.cd

    def run(self):
        venv_path = self.base_dir.joinpath(self.venv)
        if not venv_path.exists():
            raise RuntimeError(f"Venv {self.venv} doesn't exist, aborting...")

        if os.getenv("VIRTUAL_ENV"):
            self.print("dvenv")

        project = venv_path.joinpath(".project")
        if project.exists():
            if self.cd:
                with project.open() as file:
                    self.print(f"cd {file.read().strip()}")
            environment = venv_path.joinpath(".environment")
            if environment.exists():
                new_environment: dict[str, Any] = {}
                with environment.open() as file:
                    for line in file:
                        new_environment.update(SettingsParser(line.strip()).data)
                environment_string = " ".join(
                    f"{key}={value}" for key, value in new_environment.items()
                )
                self.print(f"invenv {environment_string}")

        activate = venv_path.joinpath("bin/activate")
        if activate.exists():
            self.print(f". {activate}")
        else:
            self.print(f"export VIRTUAL_ENV=dummy_{self.venv}")
