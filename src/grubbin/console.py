import asyncio

import click

from .main import run


@click.group()
def main() -> None:
    """grubbin"""


@main.command("run")
@click.option("--api-key", required=True)
@click.option("--sec-key", required=True)
@click.option("--dry-run/--no-dry-run", default=False)
def _run(api_key: str, sec_key: str, dry_run: bool = False) -> None:
    """run"""

    if dry_run:
        print("Dry run")
        return

    asyncio.run(run(api_key, sec_key))
