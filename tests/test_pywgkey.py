import os
import pathlib

import pytest

from pywgkey.key import WgKey, WgPsk
from pywgkey.utils import generate_keys_until_string_is_found, write_key_to_file


def test_WgKey():
    wanted_string = "a"
    key = generate_keys_until_string_is_found(wanted_string)
    assert wanted_string in key.pubkey.lower()
    assert key.name == wanted_string
    assert str(key) == key.pubkey


def test_WgKey_begining():
    wanted_string = "a"
    key = generate_keys_until_string_is_found(wanted_string, startswith=True)
    assert key.pubkey.lower().startswith(wanted_string)
    assert key.name == wanted_string
    assert len(key.privkey) == 44


def test_invalid_alphabet():
    wanted_string = "&"
    with pytest.raises(ValueError):
        generate_keys_until_string_is_found(wanted_string)


def test_string_too_long():
    wanted_string = "abcdef"
    with pytest.raises(ValueError):
        generate_keys_until_string_is_found(wanted_string)


def test_empty_string():
    wanted_string = ""
    with pytest.raises(ValueError):
        generate_keys_until_string_is_found(wanted_string)


def test_WgPsk():
    key = WgPsk("test")
    assert key.name == "test"
    assert len(key.key) == 44
    assert str(key) == key.key


def test_write_key_to_file(tmpdir):
    os.chdir(tmpdir)

    key = WgKey()
    key.name = "testkey"
    psk = WgPsk(key.name)

    temp_dir = pathlib.Path(tmpdir)

    privkey_path = temp_dir.joinpath(f"{key.name}.priv")
    pubkey_path = temp_dir.joinpath(f"{key.name}.pub")
    psk_path = temp_dir.joinpath(f"{key.name}.psk")

    write_key_to_file(key, psk)

    # Private key file
    assert privkey_path.is_file()
    assert oct(privkey_path.stat().st_mode).endswith("600")
    assert privkey_path.read_text() == key.privkey

    # Public key file
    assert pubkey_path.is_file()
    assert oct(pubkey_path.stat().st_mode).endswith("600")
    assert pubkey_path.read_text() == key.pubkey

    # Preshared key file
    assert psk_path.is_file()
    assert oct(psk_path.stat().st_mode).endswith("600")
    assert psk_path.read_text() == psk.key


def test_main():
    ...
