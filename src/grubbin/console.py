import click

from .main import run


@click.group()
def main():
    """grubbin"""


@main.command(name="run")
def _run():
    """run"""
    run()
