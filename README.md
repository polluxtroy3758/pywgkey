![GitHub Workflow Status](https://img.shields.io/github/workflow/status/polluxtroy3758/pywgkey/Test?style=flat-square) ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/polluxtroy3758/pywgkey?include_prereleases&style=flat-square)

# PyWgKey

A simple WireGuard key generator writen in python.

## Installation

```
pip install pywgkey
```

## Usage

```
$ python -m pywgkey -h
usage: python -m pywgkey [-h] [-b] [-w] [-p] string

Generate wg keypair containing specified string

positional arguments:
  string          The string that must be found in the pubkey

optional arguments:
  -h, --help      show this help message and exit
  -b, --begining  If the pubkey must start with the string (default: False)
  -w, --write     Write keys to files
  -p, --psk       Genarate a preshared key as well
```

### Generate and print a keypair containing a string

```
$ python -m pywgkey test
Your public key is:  1f810nNMhOB8mYpGbEvDwmXTeStPMycLiHpw0/CeL1c=
Your private key is: 75C5ahPr5UY3paWXvLRKd82EK7KWuDDJ0D9h7/p21Us=
```

### Generate and write the keys to the current folder

```
$ python -m pywgkey test -w
Keys have been writen to test.pub and test.priv
$ cat test.pub
1f810nNMhOB8mYpGbEvDwmXTeStPMycLiHpw0/CeL1c=
$ cat test.priv
75C5ahPr5UY3paWXvLRKd82EK7KWuDDJ0D9h7/p21Us=
```

### If you want the public key to **start** with a string (case is ignored)

```
$ python -m pywgkey test -b
Your public key is:  TEsTtKLgqud0Yohg8geFKcnGy99xFzZlMvSv2YbwT1Y=
Your private key is: paknyfh/d0LhZP2LqtjzJs2UE6XwaN14irxFdLV6d94=
```
