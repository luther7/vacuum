import asyncio

import click

from .logger import get_logger
from .streamer import stream
from .template import schema

logger = get_logger(__name__)


@click.group()
def main() -> None:
    pass


logger = get_logger(__name__)


@main.command("stream")
def _stream() -> None:
    asyncio.run(stream())


@main.group()
def template() -> None:
    pass


@template.command("schema")
def _schema() -> None:
    schema()
