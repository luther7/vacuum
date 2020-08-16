import asyncio

import click

from .fetcher import fetch
from .logger import get_logger
from .streamer import stream
from .template import schema
from .webserver import serve

logger = get_logger(__name__)


@click.group()
def main() -> None:
    pass


@main.command("serve")
def _serve() -> None:
    serve()


@main.command("stream")
def _stream() -> None:
    asyncio.run(stream())


@main.command("fetch")
def _fetch() -> None:
    asyncio.run(fetch())


@main.group()
def template() -> None:
    pass


@template.command("schema")
def _schema() -> None:
    schema()
