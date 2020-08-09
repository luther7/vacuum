import asyncio

import click

from .main import run


@click.group()
def main() -> None:
    """grubbin"""


@main.command("run")
@click.option("--binance-api-key", required=True)
@click.option("--binance-security-key", required=True)
@click.option("--influx-host", default="localhost")
@click.option("--influx-port", default=8086)
@click.option("--influx-user", default="admin")
@click.option("--influx-password", default="password")
@click.option("--influx-database", default="binance")
@click.option("--dry-run/--no-dry-run", default=False)
def _run(
    binance_api_key: str,
    binance_security_key: str,
    influx_host: str,
    influx_port: int,
    influx_user: str,
    influx_password: str,
    influx_database: str,
    dry_run: bool = False,
) -> None:
    """run"""

    if dry_run:
        print("Dry run")
        return

    asyncio.run(
        run(
            binance_api_key,
            binance_security_key,
            influx_host,
            influx_port,
            influx_user,
            influx_password,
            influx_database,
            dry_run,
        )
    )
