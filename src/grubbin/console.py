import asyncio

import click

from .logger import get_logger
from .main import stream

logger = get_logger(__name__)


@click.group()
def main() -> None:
    """grubbin"""


logger = get_logger(__name__)


@main.command("run")
def _run(dry_run: bool = False) -> None:
    """run"""

    if dry_run:
        logger.info("Dry run")
        return

    asyncio.run(stream())
