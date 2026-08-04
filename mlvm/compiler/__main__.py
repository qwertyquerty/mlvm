"""
MLVC Compiler CLI
"""

import os
import sys

from . import CompilerStateMachine

if len(sys.argv) < 3:
    print("You must specify an input and output file!")
    exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

cwd = os.getcwd()
csm = CompilerStateMachine(input_file, cwd)
asm = csm.generate()

print(asm)

try:
    with open(output_file, "w") as output_stream:
        output_stream.write(asm)
except OSError:
    print(f"Failed to open {output_file}!")
    exit(1)
