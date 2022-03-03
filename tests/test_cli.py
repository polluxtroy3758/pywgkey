import os
import pathlib

import pytest
from click.testing import CliRunner

from pywgkey.__main__ import main


@pytest.mark.parametrize("wanted_string, exit_code", [("a", 0), ("b", 0), (None, 2)])
def test_cli(wanted_string: str, exit_code: int):
    runner = CliRunner()
    result = runner.invoke(main, wanted_string)
    assert result.exit_code == exit_code

    if result.exit_code == 0:
        out_lines = result.output.split("\n")
        assert out_lines[0].startswith("Public key:")

        pubkey = out_lines[0].split("\t")[1]
        assert wanted_string in pubkey.lower()

        assert out_lines[1].startswith("Private key:")


@pytest.mark.parametrize("wanted_string", ["a", "b"])
def test_cli_begining(wanted_string: str):
    runner = CliRunner()
    result = runner.invoke(main, ["-b", wanted_string])
    assert result.exit_code == 0

    out_lines = result.output.split("\n")
    pubkey = out_lines[0].split("\t")[1].lower()

    assert pubkey.startswith(wanted_string)


def test_cli_psk():
    runner = CliRunner()
    result = runner.invoke(main, ["-p", "a"])
    assert result.exit_code == 0

    out_lines = result.output.split("\n")
    assert out_lines[2].startswith("Preshared key:")


def test_cli_write(tmpdir):
    os.chdir(tmpdir)

    runner = CliRunner()
    result = runner.invoke(main, ["-w", "-p", "a"])
    assert result.exit_code == 0

    assert pathlib.Path("a.pub").exists()
    assert pathlib.Path("a.priv").exists()
    assert pathlib.Path("a.psk").exists()
