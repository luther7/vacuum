import asyncio
from decimal import getcontext

import click

from .logger import get_logger
from .main import run

logger = get_logger(__name__)

getcontext().prec = 8


@click.group()
def main() -> None:
    """grubbin"""


@main.command("run")
@click.option("--binance-api-key", required=True)
@click.option("--binance-security-key", required=True)
@click.option("--bitforex-api-key", required=True)
@click.option("--bitforex-security-key", required=True)
@click.option("--postgres-host", default="localhost")
@click.option("--postgres-port", default=5432)
@click.option("--postgres-user", default="postgres")
@click.option("--postgres-password", default="password")
@click.option("--postgres-database", default="grubbin")
@click.option("--dry-run/--no-dry-run", default=False)
def _run(
    binance_api_key: str,
    binance_security_key: str,
    bitforex_api_key: str,
    bitforex_security_key: str,
    postgres_host: str,
    postgres_port: int,
    postgres_user: str,
    postgres_password: str,
    postgres_database: str,
    dry_run: bool = False,
) -> None:
    """run"""

    if dry_run:
        logger.info("Dry run")
        return

    asyncio.run(
        run(
            binance_api_key,
            binance_security_key,
            bitforex_api_key,
            bitforex_security_key,
            postgres_host,
            postgres_port,
            postgres_user,
            postgres_password,
            postgres_database,
            dry_run,
        )
    )
