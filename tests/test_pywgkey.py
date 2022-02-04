import pytest

from pywgkey import __version__
from pywgkey.utils import generate_keys_until_string_is_found


def test_version():
    assert __version__ == "0.1.0"


def test_WgKey():
    wanted_string = "a"
    key = generate_keys_until_string_is_found(wanted_string)
    assert wanted_string in key.pubkey.lower()
    assert key.name == wanted_string


def test_WgKey_begining():
    wanted_string = "a"
    key = generate_keys_until_string_is_found(wanted_string, startswith=True)
    assert key.pubkey.lower().startswith(wanted_string)
    assert key.name == wanted_string


def test_invalid_alphabet():
    wanted_string = "&"
    with pytest.raises(ValueError):
        generate_keys_until_string_is_found(wanted_string)


def test_string_tool_long():
    wanted_string = "abcdef"
    with pytest.raises(ValueError):
        generate_keys_until_string_is_found(wanted_string)


def test_empty_string():
    wanted_string = ""
    with pytest.raises(ValueError):
        generate_keys_until_string_is_found(wanted_string)
