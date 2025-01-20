import argparse
import ecdsa
from ecdsa.util import sigdecode_string, sigencode_string
from hashlib import sha256

DEMO_PRIVATE_KEY = 'f94a840f1e1a901843a75dd07ffcc5c84478dc4f987797474c9393ac53ab55e6'
DEMO_NONCE = '75bcd15'
DEMO_MESSAGE = 'test-1'

def verify_signature(public_key, signature, message):
    '''
    Verifies message signature.

    We try to determine the random point given the public key, signature and message.
    Remember that the signature contains the x-coordinate of the random point.

    R = (s⁻¹ * z) * G + (s⁻¹ * r) * Q

    s: Second part of the signature
    z: Message hash
    r: x-coordinate of random point
    Q: Public key

    Built-in alternative:
    sig_enc = sigencode_string(signature[0], signature[1], ecdsa.SECP256k1.order)
    return public_key.verify(sig_enc, message.encode('utf-8'), hashfunc=sha256) # raises exception if invalid
    '''
    # Invert s (for division)
    s_inv = ecdsa.numbertheory.inverse_mod(signature[1], ecdsa.SECP256k1.order)
    message_hash = sha256(message.encode('utf-8')).hexdigest()
    z = int(message_hash, 16)
    r = signature[0]

    final = (s_inv * z) * ecdsa.SECP256k1.generator + (s_inv * r) * public_key.pubkey.point

    return final.x() == r

def private_key_from_hex(private_key_hex: str):
    private_key_bytes = bytes.fromhex(private_key_hex)

    return ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

def sign_message(private_key_hex: str, nonce_hex: str, message: str):
    '''
    Sign message.

    s = k⁻¹ * (z + r * d)

    k: Nonce
    z: Message hash
    r: x-coordinate of random point
    d: Private key

    Make sure to take the lower s value.

    Built-in alternative:
    signature = private_key.sign(message.encode('utf-8'), hashfunc=sha256, k=k)
    (r, s) = sigdecode_string(signature, ecdsa.SECP256k1.order) # (int.from_bytes(signature[:32], "big"), int.from_bytes(signature[32:], "big"))
    '''
    message_hex = sha256(message.encode('utf-8')).hexdigest()
    k = int(nonce_hex, 16)
    random_point = k * ecdsa.SECP256k1.generator
    n = ecdsa.SECP256k1.order

    # Generate r and s values
    r = random_point.x()
    s = (ecdsa.numbertheory.inverse_mod(k, n) * (int(message_hex, 16) + (int(private_key_hex, 16) * random_point.x()) % n)) % n

    # s can be high or low (i.e. in the upper or lower half of the curve)
    # Since BIP62 Bitcoin transactions only use low-s values
    # So if s is above half the curve: negate it
    if s > n / 2:
        s = n - s

    return (r, s)

def recover_private_key(msg1, msg2, sig1, sig2):
    '''
    Recover the private key from two messages and their signatures.

    How it works:

    z = Message hash
    r = x-coordinate of random point (first part of the signature)
    s = Second part of the signature
    n = Curve order
    d = Private key

    Use
    s₁ = k⁻¹(z₁ + r * d) mod n
    and
    s₂ = k⁻¹(z₂ + r * d) mod n
    to get
    k = (z₁ - z₂) * (s₁ - s₂)⁻¹ mod n

    Use
    s₁ = k⁻¹(z₁ + r * d) mod n
    and
    k = (z₁ - z₂) * (s₁ - s₂)⁻¹ mod n
    to get
    d = (k * s₁ - z₁) * r⁻¹ mod n

    See README for more details.
    '''
    # SHA256 hash each message
    z1_hex = sha256(msg1.encode('utf-8')).hexdigest()
    z2_hex = sha256(msg2.encode('utf-8')).hexdigest()

    n = ecdsa.SECP256k1.order
    z1 = int(z1_hex, 16)
    z2 = int(z2_hex, 16)
    r1 = sig1[0]
    r2 = sig2[0]
    s1 = sig1[1]
    s2 = sig2[1]

    # BIP62: Bitcoin transaction signatures always use the low-s value
    # But because we don't know whether the "original" s-value was high or low, we try all combinations
    s1_set = [s1, n - s1]
    s2_set = [s2, n - s2]

    possibilities = []

    for s1_value in s1_set:
        for s2_value in s2_set:
            # Calculate nonce
            k = ((z1 - z2) * ecdsa.numbertheory.inverse_mod(s1_value - s2_value, n)) % n

            # Calculate private key
            d = (k * s1_value - z1) * ecdsa.numbertheory.inverse_mod(r1, n) % n
            d_hex = hex(d)[2:].zfill(64)

            possibilities.append((k, d_hex))

    return possibilities

def parse_arguments():
  parser = argparse.ArgumentParser(description='Bitcoin Transaction Signer')

  parser.add_argument('--private_key', action="store", dest='private_key', type=str, default=DEMO_PRIVATE_KEY)
  parser.add_argument('--nonce', action="store", dest='nonce', type=str, default=DEMO_NONCE)
  parser.add_argument('--message', action="store", dest='message', type=str, default=DEMO_MESSAGE)

  return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    print()
    print('### Signing ###')
    print()

    # Sign message
    signature1 = sign_message(args.private_key, args.nonce, args.message)
    verified1 = verify_signature(private_key_from_hex(args.private_key).get_verifying_key(), signature1, args.message)

    print('Signature 1:')
    print(f'    r: {signature1[0]}')
    print(f'    s: {signature1[1]}')
    print(f'Verified: {verified1}')
    print()

    # Sign another message using the same nonce
    message2 = 'test-2'
    signature2 = sign_message(args.private_key, args.nonce, message2)
    verified2 = verify_signature(private_key_from_hex(args.private_key).get_verifying_key(), signature1, args.message)

    print('Signature 2:')
    print(f'    r: {signature2[0]}')
    print(f'    s: {signature2[1]}')
    print(f'Verified: {verified2}')

    # Recover private key
    recovered_private_key = recover_private_key(args.message, message2, signature1, signature2)

    print()
    print('### Recovery ###')
    print()

    print('Possible nonces (k) and private keys (d):')
    print()

    for k, d in recovered_private_key:
        print(f'k: {k}')
        print(f'd: {d}')
        print()