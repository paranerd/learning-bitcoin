import random
from hashlib import pbkdf2_hmac, sha256

WORDLIST_FILENAME = 'bip39-wordlist.txt'
SEED_SIZE_BIT = 64
PASSPHRASE = '[passphrasegoeshere]'

def generate_entropy(length):
  return ''.join([str(random.randint(0, 1)) for i in range(length)])

def hex_to_binary(hex_str):
  # Prepends a '1' to the input, then strips it from the output to not lose leading binary zeros
  return bin(int('1' + hex_str, 16))[3:]

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
  return sha256(entropy.encode('utf-8')).hexdigest()

def generate_salt(passphrase):
  return ('mnemonic' + passphrase).encode('utf-8')

def generate_seed(mnemonic):
  return pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), salt, 2048)

if __name__ == "__main__":
  # Generate entropy
  entropy = generate_entropy(SEED_SIZE_BIT)
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