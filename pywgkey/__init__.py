"""This module is made to generate keys for Wireguard.

It's specificity is to require an input string, which must be present in the
public part of the key.

Please note that this may weaken the Wireguard configuration, as keys may be
more predictable.
"""

from .key import WgKey, WgPsk  # noqa: F401

__version__ = "0.2.1"
