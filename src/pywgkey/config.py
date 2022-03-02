"""Global configuration for the module"""

from string import ascii_letters, digits

MAX_LENGTH = 5
BASE64_ALPHABET = list(ascii_letters) + list(digits) + ["/", "+"]
