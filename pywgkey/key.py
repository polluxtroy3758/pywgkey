"""Main classes used in the module"""

from base64 import b64encode

from nacl.public import PrivateKey as _PrivateKey


class WgKey:
    """Wireguard key pair"""

    def __init__(self):
        self._key = _PrivateKey.generate()
        self._name = None

    def __str__(self) -> str:
        return self.pubkey

    @property
    def pubkey(self) -> str:
        """The base 64 encoded public key"""
        return b64encode(bytes(self._key.public_key)).decode("ascii")

    @property
    def privkey(self) -> str:
        """The base 64 encoded private key"""
        return b64encode(bytes(self._key)).decode("ascii")

    @property
    def name(self):
        """The name of the key

        Based on the string searched in the public key.
        """
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value


class WgPsk:
    """Wireguard preshared key"""

    def __init__(self, name: str = None):
        self._key = _PrivateKey.generate()
        self._name = name

    def __str__(self):
        return self.key

    @property
    def key(self) -> str:
        """The base 64 encoded preshared key"""
        return b64encode(bytes(self._key)).decode("ascii")

    @property
    def name(self) -> str:
        """The name of the key

        Based on the string searched in the public key.
        """
        return f"{self._name}"
