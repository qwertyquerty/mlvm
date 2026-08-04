"""
MLVM Assembler CLI
"""

import sys

from . import assemble

if len(sys.argv) < 3:
    print("You must specify an input and output file!")
    exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    with open(input_file, "r") as input_stream:
        mlvm_script = input_stream.read()
except OSError:
    print(f"Failed to open {input_file}!")
    exit(1)

output_bytes = assemble(mlvm_script)

try:
    with open(output_file, "wb") as output_stream:
        output_stream.write(output_bytes)
except OSError:
    print(f"Failed to open {output_file}!")
    exit(1)
