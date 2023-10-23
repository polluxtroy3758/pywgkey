"""This file is used when the module is called directly
"""

import click

from .key import WgPsk
from .utils import (
    generate_keys_until_string_is_found,
    generate_public_key_from_private_key,
    print_keys,
    write_key_to_file,
)


@click.command()
@click.argument("wanted_string", type=str, required=True)
@click.option(
    "-b", "--begining", is_flag=True, help="If the pubkey must start with the string."
)
@click.option("-w", "--write", is_flag=True, help="Write keys to files.")
@click.option("-p", "--psk", is_flag=True, help="Genarate a preshared key as well.")
def full(wanted_string: str, begining: bool, write: bool, psk: bool):
    """Generate WireGuard keypair containing specified wanted string."""

    key = generate_keys_until_string_is_found(wanted_string, begining)

    pre_shared_key = None
    if psk:
        pre_shared_key = WgPsk(wanted_string)

    if write:
        write_key_to_file(key, pre_shared_key)
    else:
        print_keys(key, pre_shared_key)


@click.command()
@click.argument("private_key", type=str, required=True)
def pub(private_key):
    """Retrieve public key from a private key."""
    key = generate_public_key_from_private_key(private_key)
    print_keys(key)


@click.group()
def cli():
    """Wireguard key generation tool."""
    pass


cli.add_command(full)
cli.add_command(pub)


if __name__ == "__main__":  # pragma: no cover
    cli()
