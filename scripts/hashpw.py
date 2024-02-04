import bcrypt
import sys

if len(sys.argv) < 2:
    raise Exception('Value to hash is required')

value_to_hash = str(sys.argv[1]).encode()
hashed_value = bcrypt.hashpw(value_to_hash, bcrypt.gensalt())
print(hashed_value.decode())
