import asyncio

import click

from .logger import get_logger
from .main import stream
from .template import schema

logger = get_logger(__name__)


@click.group()
def main() -> None:
    pass


logger = get_logger(__name__)


@main.command("run")
def _run() -> None:
    asyncio.run(stream())


@main.group()
def template() -> None:
    pass


@template.command("schema")
def _schema() -> None:
    schema()
