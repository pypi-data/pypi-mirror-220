import argparse
import asyncio
from . import utils as utils
from .core import command as command, formatter as formatter
from .core.config import Config as Config
from .core.context import Context as Context, GroupResolver as GroupResolver
from .core.plugin import Plugin as Plugin, search_plugins as search_plugins
from _typeshed import Incomplete
from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple

parser: Incomplete
group: Incomplete
PROMPT: str

class PidFileType(argparse.FileType):
    def __call__(self, string): ...

context: Incomplete

def main(*config_files: str, args: Optional[argparse.Namespace] = ..., config_dirs: Sequence[Path] = ..., commands: Tuple[str, ...] = ..., config_dict: Optional[Mapping] = ...): ...
def process_iter(cfg, cpus=...): ...
def create_process(cfg): ...
def loop_run(conf: Optional[Mapping] = ..., future: Optional[asyncio.Future] = ..., group_resolver: Optional[GroupResolver] = ..., ns: Optional[argparse.Namespace] = ..., cmds: Sequence[str] = ..., argv: Sequence[str] = ..., loop: Optional[asyncio.AbstractEventLoop] = ..., prompt: Optional[str] = ..., process_name: Optional[str] = ...): ...

class UriType(argparse.FileType):
    def __call__(self, string): ...

class plugin(Plugin):
    def add_arguments(self, parser: argparse.ArgumentParser): ...

def main_with_conf(*args, **kwargs) -> None: ...
