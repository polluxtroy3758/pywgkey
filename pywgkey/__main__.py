"""This file is used when the module is called directly
"""

import argparse
import sys

from .key import WgPsk
from .utils import (
    generate_keys_until_string_is_found,
    print_keys,
    validate_string,
    write_key_to_file,
)


def main(args: argparse.Namespace):
    """Main function used when calling module directly"""

    validate_string(args.string)

    key = generate_keys_until_string_is_found(args.string, args.begining)

    psk = None
    if args.psk:
        psk = WgPsk(args.string)

    if args.write:
        write_key_to_file(key, psk)
    else:
        print_keys(key, psk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate wg keypair containing specified string",
        prog="python -m pywgkey",
    )
    parser.add_argument(
        "string", type=str, help="The string that must be found in the pubkey"
    )
    parser.add_argument(
        "-b",
        "--begining",
        action="store_true",
        help="If the pubkey must start with the string (default: False)",
    )
    parser.add_argument(
        "-w", "--write", action="store_true", help="Write keys to files"
    )
    parser.add_argument(
        "-p", "--psk", action="store_true", help="Genarate a preshared key as well"
    )
    args = parser.parse_args()

    sys.exit(main(args))
