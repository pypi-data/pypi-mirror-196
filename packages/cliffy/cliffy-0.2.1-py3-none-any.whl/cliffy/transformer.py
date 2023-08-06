## Transformer

import os
import pathlib
import sys
from typing import TextIO

import yaml

from .commander import build_cli
from .commanders.typer import TyperCommander

PYTHON_BIN = f"{sys.exec_prefix}/bin"
PYTHON_EXECUTABLE = sys.executable
CLIFFY_CLI_DIR = f"{pathlib.Path(__file__).parent.resolve()}/clis"


class Transformer:
    """Loads command manifest and transforms it into a CLI"""

    def __init__(self, manifest: TextIO) -> None:
        self.manifest: TextIO = manifest
        self.command_config: dict = self.load_manifest()
        self.cli: str = ""

    def render_cli(self) -> None:
        self.cli = build_cli(self.command_config, commander_cls=TyperCommander)
        return self.cli

    def load_cli(self) -> str:
        self.render_cli()
        self.deploy_script()
        self.deploy_cli()
        return self.cli

    def load_manifest(self) -> dict:
        try:
            return yaml.safe_load(self.manifest)
        except yaml.YAMLError as e:
            print("load_manifest", e)

    def deploy_cli(self) -> bool:
        cli_path = f"{CLIFFY_CLI_DIR}/{self.command_config['name']}.py"
        write_to_file(cli_path, self.cli.code)

    def deploy_script(self) -> bool:
        script_path = f"{PYTHON_BIN}/{self.command_config['name']}"
        write_to_file(script_path, self.get_cli_script(), executable=True)

    def get_cli_script(self) -> None:
        return f"""#!{PYTHON_EXECUTABLE}
import sys
from cliffy.clis.{self.command_config['name']} import cli

if __name__ == '__main__':
    sys.exit(cli())"""


def write_to_file(path, text, executable=False) -> bool:
    try:
        with open(path, "w") as s:
            s.write(text)
    except Exception as e:
        print("write_to_file", e)
        return False

    if executable:
        make_executable(path)

    return True


def make_executable(path) -> None:
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)
