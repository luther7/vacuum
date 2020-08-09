# import pytest

from click.testing import CliRunner
from grubbin.console import main


def test_example():
    command = ["run"]

    runner = CliRunner()
    result = runner.invoke(main, command)

    assert "run" in result.output
    assert result.exit_code == 0
