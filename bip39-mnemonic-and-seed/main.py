import random
from hashlib import pbkdf2_hmac, sha256
import secrets

WORDLIST_FILENAME = 'bip39-wordlist.txt'
ENTROPY_BITS = 128
PASSPHRASE = 'TREZOR'

def generate_entropy(length=ENTROPY_BITS):
  # Alternative 1: Generate each bit step-by-step:
  # ''.join([str(random.randint(0, 1)) for i in range(length)])

  # Alternative 2: Use secrets.randbits
  # entropy_int = secrets.randbits(length)
  # return bin(entropy_int)[2:].zfill(length)

  entropy_hex = secrets.token_hex(int(length / 8))
  entropy_int = int(entropy_hex, 16)

  return bin(entropy_int)[2:].zfill(length)

def hex_to_binary(hex_str):
  # Alternative: Prepend a '1' to the input, then strips it from the output to not lose leading binary zeros:
  # return bin(int('1' + hex_str, 16))[3:]

  # Every hex character represents 4 bit ('ffff' = 15), so the binary representation must be padded to 4 times the hex length
  return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)

def split_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def load_wordlist(filename):
  with open(filename, 'r') as f:
    return f.read().splitlines()

def generate_mnemonic(chunks):
  wordlist = load_wordlist(WORDLIST_FILENAME)
  seed = []

  for chunk in chunks:
    index = int(chunk, 2)
    seed.append(wordlist[index])

  return ' '.join(seed)

def calculate_fingerprint(entropy):
  """
  Calculates entropy's SHA256 fingerprint.

  Converts entropy from binary string to integer to hex to bytes.
  Makes sure to pad hex to not lose leading zeros.
  Returns SHA256 hash from bytes.
  """
  entropy_length_hex = int(len(entropy) / 4)

  return sha256(bytes.fromhex(hex(int(entropy, 2))[2:].zfill(entropy_length_hex))).hexdigest()

def generate_salt(passphrase):
  return ('mnemonic' + passphrase).encode('utf-8')

def generate_seed(mnemonic):
  return pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), salt, 2048)

if __name__ == "__main__":
  # Generate entropy
  entropy = generate_entropy()
  print(f'Entropy: {entropy}')

  # Calculate fingerprint
  fingerprint_hex = calculate_fingerprint(entropy)
  print(f'Fingerprint: {fingerprint_hex}')

  fingerprint_binary = hex_to_binary(fingerprint_hex)
  print(f'Fingerprint binary: {fingerprint_binary}')

  # Get checksum
  checksum_length = int(len(entropy) / 32)
  print(f'Checksum length: {checksum_length}')

  checksum = fingerprint_binary[:checksum_length]
  print(f'Checksum: {checksum}')

  # Add checksum to entropy
  entropy_with_checksum = entropy + checksum
  print(f'Entropy with checksum: {entropy_with_checksum}')

  # Chunk to 11 bits
  chunks = split_list(entropy_with_checksum, 11)
  print(f'Chunks: {chunks}')

  # Generate mnemonic
  mnemonic = generate_mnemonic(chunks)
  print()
  print(f'Mnemonic: {mnemonic}')

  # Generate seed
  salt = generate_salt(PASSPHRASE)
  seed = generate_seed(mnemonic)
  print(f'Seed: {seed.hex()}')