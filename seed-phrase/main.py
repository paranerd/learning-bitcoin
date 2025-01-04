import random
from hashlib import sha256

WORDLIST_FILENAME = 'bip39-wordlist.txt'
SEED_SIZE = 64

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

def generate_seed_phrase(chunks):
  wordlist = load_wordlist(WORDLIST_FILENAME)
  seed = []

  for chunk in chunks:
    index = int(chunk, 2)
    seed.append(wordlist[index])

  return ' '.join(seed)

if __name__ == "__main__":
  # Generate entropy
  entropy = generate_entropy(SEED_SIZE)
  print(f'Entropy: {entropy}')

  # Calculate fingerprint
  fingerprint_hex = sha256(entropy.encode('utf-8')).hexdigest()
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

  chunks = split_list(entropy_with_checksum, 11)
  print(f'Chunks: {chunks}')

  seed_phrase = generate_seed_phrase(chunks)
  print()
  print(f'Seed phrase: {seed_phrase}')