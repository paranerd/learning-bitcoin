# How long does it take to generate two identical private keys?

A Bitcoin private key is a 256-bit hash and can be represented as any number between 1 and 115792089237316195423570985008687907852837564279074904382605163141518161494336.

That number is slighly below the maximum value that a 256-bit hash _could_ represent.

This is due to the elliptic curve used in Bitcoin (secp256k1) which has n number of points of which Bitcoin uses n-1.

Using 1,000,000 computers calculating 1,000,000 keys per second it would still take roughly a staggering 3671743063080803235470924132853876261056103149731840 years to create a collision.