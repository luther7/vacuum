# import pytest

from click.testing import CliRunner
from grubbin.console import main


def test_example():
    command = ["example"]

    runner = CliRunner()
    result = runner.invoke(main, command)

    assert "grubbin example" in result.output
    assert result.exit_code == 0
