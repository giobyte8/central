import bcrypt
import sys

if len(sys.argv) < 2:
    raise Exception('Value to hash is required')

raw_input = str(sys.argv[1])
print(f'Input: { raw_input }')

hashed_value = bcrypt.hashpw(raw_input.encode(), bcrypt.gensalt())
print(hashed_value.decode())
