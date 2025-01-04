# How to create a BIP 39 mnemonic sentence

1. Generate random entropy
1. Calculate entropy's fingerprint
1. Add checksum from fingerprint to entropy
1. Split result into 11 bit chunks
1. Turn chunks into integer indices
1. Get words from wordlist at those indices