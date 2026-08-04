"""
MLVM Virtual Machine CLI
"""

import sys

from mlvm.vm import build_machine, run

if len(sys.argv) < 2:
    print("You must specify an input rom!")
    exit(1)

try:
    machine = build_machine(sys.argv[1])
except OSError:
    print(f"Failed to open {sys.argv[1]}!")
    exit(1)

run(machine)
