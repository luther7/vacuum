import click


@click.group()
def main():
    """grubbin console"""


@main.command()
def example():
    """grubbin example"""
    print("grubbin example")
