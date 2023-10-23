import os
import pathlib

import pytest
from click.testing import CliRunner

from pywgkey.__main__ import cli


@pytest.mark.parametrize("wanted_string, exit_code", [("a", 0), ("b", 0), (None, 1)])
def test_cli(wanted_string: str, exit_code: int):
    runner = CliRunner()
    result = runner.invoke(cli, ["full", wanted_string])
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
    result = runner.invoke(cli, ["full", "-b", wanted_string])
    assert result.exit_code == 0

    out_lines = result.output.split("\n")
    pubkey = out_lines[0].split("\t")[1].lower()

    assert pubkey.startswith(wanted_string)


def test_cli_psk():
    runner = CliRunner()
    result = runner.invoke(cli, ["full", "-p", "a"])
    assert result.exit_code == 0

    out_lines = result.output.split("\n")
    assert out_lines[2].startswith("Preshared key:")


def test_cli_write(tmpdir):
    os.chdir(tmpdir)

    runner = CliRunner()
    result = runner.invoke(cli, ["full", "-w", "-p", "a"])
    assert result.exit_code == 0

    assert pathlib.Path("a.pub").exists()
    assert pathlib.Path("a.priv").exists()
    assert pathlib.Path("a.psk").exists()


@pytest.mark.parametrize("answer, exit_code", [("y", 0), ("n", 0), ("", 1), ("a", 1)])
def test_cli_overwrite_files(tmpdir, answer, exit_code):
    os.chdir(tmpdir)
    pubkey_file = pathlib.Path("a.pub")
    pubkey_file.touch()

    runner = CliRunner()
    result = runner.invoke(cli, ["full", "-w", "-p", "a"], input=answer)
    assert result.exit_code == exit_code


def test_cli_file_not_writable(tmpdir):
    os.chdir(tmpdir)
    pubkey_file = pathlib.Path("a.pub")
    pubkey_file.touch(0o100)

    runner = CliRunner()
    result = runner.invoke(cli, ["full", "-w", "a"])
    assert result.exception


def test_cli_file_is_directory(tmpdir):
    os.chdir(tmpdir)
    pubkey_file = pathlib.Path("a.pub")
    pubkey_file.mkdir()

    runner = CliRunner()
    result = runner.invoke(cli, ["full", "-w", "a"])
    assert result.exception


def test_cli_file_parent_not_writeable(tmpdir):
    os.chdir(tmpdir)
    pathlib.Path().cwd().chmod(0o100)

    runner = CliRunner()
    result = runner.invoke(cli, ["full", "-w", "a"])
    assert result.exception
