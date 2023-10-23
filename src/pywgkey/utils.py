"""Utilities functions"""

import os
import pathlib
from typing import Union

from .config import BASE64_ALPHABET, MAX_LENGTH
from .key import WgKey, WgPsk


def validate_string(wanted_string: str):
    """Validate a given string.

    If the given `wanted_string` is composed of valid base 64 characters **AND** it's
    length is not longer than `MAX_LENGTH`, then it is valid.

    Any invalid `wanted_string` will raise a `ValueError` exception.

    :param str wanted_string: the string to validate as valid base64 characters
    :raises ValueError: if string is not valid
    """
    if wanted_string == "":
        raise ValueError("The string is empty.")
    if len(wanted_string) > MAX_LENGTH:
        raise ValueError(f"'{wanted_string}' is longer than {MAX_LENGTH} characters.")
    for char in wanted_string:
        if char not in BASE64_ALPHABET:
            raise ValueError("The string must only contain base 64 alphabet.")


def __string_is_found(wanted_string: str, key: WgKey, startswith: bool = False) -> bool:
    """Search for a given string in the public key of a WireGuard key pair.

    :param str wanted_string: the string to search for
    :param WgKey key: a WireGuard key pair
    :param str startswith: set to `True` if the pubkey must start with the string
    (default: `False`)
    :return: `True` if the string is found, `False` otherwise
    :rtype: bool
    """
    found = False

    if startswith:
        if key.pubkey.lower().startswith(wanted_string):
            found = True
    else:
        if wanted_string.lower() in key.pubkey.lower():
            found = True

    return found


def generate_keys_until_string_is_found(
    wanted_string: str, startswith: bool = False
) -> WgKey:
    """Generates keys until `wanted_string` is found at desired place in a pubkey.

    The `wanted_string` is first validated with the `validate_string` function, then
    keys are generated until the public key contains the string.

    Then, the key name is set to `wanted_string`.

    :param str wanted_string: string to search
    :param bool startswith: set to `True` if the key must start with the string
    :return: the matching keypair
    :rtype: WgKey
    """
    validate_string(wanted_string)
    key = WgKey()
    while not __string_is_found(wanted_string, key, startswith):
        key = WgKey()

    key.name = wanted_string  # Set the key name with the found string
    return key


def generate_public_key_from_private_key(private_key: str) -> WgKey:
    """Generate the public key from the given private key.

    :param str private_key: the given private key
    :return: the keypair
    :rtype: WgKey
    """
    return WgKey(private_key)


def __prompt_overwrite(filename: str) -> bool:
    """Prompt if the given file should be overwritten.

    :param str filename: the filename
    :return: `True` if answered `y`, `False` if answered `n` or nothing
    :rtype: bool
    """
    prompt = input(f"Should '{filename}' be overwritten? [y/N] ")
    if prompt.lower() == "y":
        return True
    elif prompt.lower() in ("n", ""):
        return False
    else:
        return __prompt_overwrite(filename)


def __can_write_file(filename: str) -> bool:
    """Check if key files already exist.

    :param str filename: the name of the file
    :return: True or False
    :rtype: bool
    :raises IOError: cannot write file
    """
    file_path = pathlib.Path(filename)

    if file_path.exists():
        if file_path.is_file():
            if os.access(file_path, os.W_OK):
                # The file exists and is writable
                return __prompt_overwrite(filename)
            else:
                raise IOError(f"File '{filename}' is not writable.")
        else:
            # It is a directory, cannot write
            raise IOError(f"'{filename}' is a directory.")
    else:
        # The file does not exists, check parent dir permissions
        if os.access(file_path.parent, os.W_OK):
            return True
        else:
            raise IOError(f"'{file_path.parent}' directory is not writable.")


def __set_file_permissions(filename: str):
    """Set file permissions to 600.

    The files persmissions are set read/write for owner (600).

    *Only posix system are supported right now.*

    :param str name: the filename to set permissions
    """
    if os.name == "posix":
        os.chmod(os.path.abspath(filename), 0o600)
    elif os.name == "nt":
        pass  # TODO: manage windows permissions


def write_key_to_file(key: WgKey, psk: Union[WgPsk, None] = None):
    """Writes the public and private key to separate files

    The public key will be saved as `<key.name>.pub`.
    The private key will be saved as `<key.name>.priv`.
    The preshared key (if any) will be saved as `<key.name>.psk`.

    :param WgKey key: the keypair to save
    :param Union[WgPsk, None] psk: the (optional) preshared key to write
    """

    files = {"pub": f"{key.name}.pub", "priv": f"{key.name}.priv"}
    if psk is not None:
        files["psk"] = f"{key.name}.psk"

    for key_type, file in files.items():
        if __can_write_file(file):
            with open(file, "w") as f:
                if key_type == "pub":
                    f.write(key.pubkey)
                    print(key.pubkey)
                elif key_type == "priv":
                    f.write(key.privkey)
                    print(key.privkey)
                elif key_type == "psk" and psk is not None:
                    f.write(psk.key)
                    print(psk.key)

            __set_file_permissions(file)
            print(f"{key_type} key have been writen to {file}\n")


def print_keys(key: WgKey, psk: Union[WgPsk, None] = None):
    """Prints the keys to stdout

    :param WgKey key: The keypair to print
    :param Union[WgPsk, None] psk: The preshared key to print
    """
    print(f"Public key:\t{key.pubkey}")
    print(f"Private key:\t{key.privkey}")
    if psk is not None:
        print(f"Preshared key:\t{psk.key}")
