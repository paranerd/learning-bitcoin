import argparse
import ecdsa
import hashlib
import hmac

DEFAULT_SEED = '5b7832b844ed7c613d9a93e7272a77788aa4a38facc8df925e890c41869570196f0679d0830d0e3285df076a05540feff16c877b2a56f3890758bdee1d16555f'
DEFAULT_CHILD_INDEX = 0

def generate_master_extended_key(seed):
  return hmac.new(b'Bitcoin seed', bytes.fromhex(seed), hashlib.sha512).hexdigest()

def generate_master_public_key(master_private_key):
  # Convert master private key to an ECDSA private key object
  master_private_key_bytes = bytes.fromhex(master_private_key) 
  signing_key = ecdsa.SigningKey.from_string(master_private_key_bytes, curve=ecdsa.SECP256k1)  

  # Get the corresponding ECDSA public key object
  verifying_key = signing_key.get_verifying_key()

  # Serialize the public key to bytes
  master_public_key_bytes = verifying_key.to_string("compressed")

  # Convert to hexadecimal
  return master_public_key_bytes.hex()

def generate_master_intermediate_key(master_public_key, master_chain_code, index):
  data = int(master_public_key, 16) + index

  return hmac.new(master_chain_code.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()

def generate_intermediate_keys(parent_public_key: bytes, parent_chain_code: bytes, index: int):
    """
    Derives the child chain code from the parent extended key.

    Args:
        parent_chain_code: The parent's chain code as bytes.
        parent_public_key: The parent's compressed public key as bytes.
        index: The index of the child key.

    Returns:
        The child chain code as bytes.
    """

    # Convert index to 4-byte big-endian bytes
    index_bytes = index.to_bytes(4, 'big')

    # Concatenate parent public key and index
    data = parent_public_key + index_bytes

    # Calculate HMAC-SHA512
    intermediate_key = hmac.new(parent_chain_code, data, hashlib.sha512).hexdigest()

    # Return left and right part separately
    return (intermediate_key[:64], intermediate_key[64:])

def generate_child_private_key(il: str, parent_private_key_bytes: bytes):
    # Convert il from hex to int
    il_int = int.from_bytes(bytes.fromhex(il), 'big')

    # Child Private Key Derivation
    child_private_key = (il_int + int.from_bytes(parent_private_key_bytes, 'big')) % ecdsa.SECP256k1.order
    
    return child_private_key.to_bytes(32, 'big')

def generate_child_public_key(child_private_key_bytes):
    signing_key = ecdsa.SigningKey.from_string(child_private_key_bytes, curve=ecdsa.SECP256k1)  

    # Get the corresponding ECDSA public key object
    verifying_key = signing_key.get_verifying_key()

    # Serialize the public key to bytes
    child_public_key_bytes = verifying_key.to_string("compressed")

    return child_public_key_bytes

def derive_child_keys(parent_private_key, parent_public_key, parent_chain_code, index):
    # Convert from hex to bytes
    parent_private_key_bytes = bytes.fromhex(parent_private_key)
    parent_public_key_bytes = bytes.fromhex(parent_public_key)
    parent_chain_code_bytes = bytes.fromhex(parent_chain_code)

    # Generate Intermediate Keys
    il, child_chain_code = generate_intermediate_keys(parent_public_key_bytes, parent_chain_code_bytes, index)

    # Generate Private Key
    child_private_key_bytes = generate_child_private_key(il, parent_private_key_bytes)

    # Generate Public Key
    child_public_key_bytes = generate_child_public_key(child_private_key_bytes)

    return (child_private_key_bytes.hex(), child_public_key_bytes.hex(), child_chain_code)

def generate_master_keys(seed):
  # Generate Master extended key
  master_extended_key = generate_master_extended_key(seed)

  # Derive Master private key and Master chain code from Master extended key
  master_private_key = master_extended_key[:64]
  master_chain_code = master_extended_key[64:]

  # Derive Master public key from Master private key
  master_public_key = generate_master_public_key(master_private_key)

  return (master_extended_key, master_private_key, master_chain_code, master_public_key)

def parse_arguments():
  parser = argparse.ArgumentParser(description='Short sample app')
  parser.add_argument('--seed', action="store", dest='seed', type=str, default=DEFAULT_SEED)
  parser.add_argument('--child_index', action="store", dest='child_index', type=int, default=DEFAULT_CHILD_INDEX)

  return parser.parse_args()

if __name__ == "__main__":
  # Parse arguments
  args = parse_arguments()

  # Generate master keys
  master_extended_key, master_private_key, master_chain_code, master_public_key = generate_master_keys(args.seed)

  print(f'Master private key: {master_private_key}')
  print(f'Master chain code: {master_chain_code}')
  print(f'Master public key: {master_public_key}')
  print()

  # Generate child keys
  child_private_key, child_public_key, child_chain_code = derive_child_keys(master_private_key, master_public_key, master_chain_code, args.child_index)

  print(f'Child {args.child_index} Chain Code: {child_chain_code}')
  print(f'Child {args.child_index} Private Key: {child_private_key}')
  print(f'Child {args.child_index} Public Key: {child_public_key}')