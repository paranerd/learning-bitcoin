# How to create a BIP 39 mnemonic sentence and seed

The "official" Python implementation can be found [here](https://github.com/trezor/python-mnemonic/blob/master/src/mnemonic/mnemonic.py).

1. Generate random 64 bits of entropy
1. Calculate entropy's fingerprint using SHA256
1. Add checksum from fingerprint to entropy
1. Split result into 11 bit chunks
1. Turn chunks into integer indices
1. Get words from wordlist at those indices
1. Calculate 64 byte seed using mnemonic's (and optional passphrase's) PBKDF2 HMAC