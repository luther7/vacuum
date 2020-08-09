# import pytest

from click.testing import CliRunner
from grubbin.console import main


def test_example():
    command = ["run", "--api-key=1", "--sec-key=1", "--dry-run"]

    runner = CliRunner()
    result = runner.invoke(main, command)

    assert "Dry run" in result.output
    assert result.exit_code == 0
