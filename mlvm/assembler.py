import re
import mlvm.instructions
from mlvm.const import *
import sys

if len(sys.argv) < 3:
    print("You must specify an input and output file!")
    exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    with open(input_file, "r") as input_stream:
        mlvm_script = input_stream.read()
except:
    print(f"Failed to open {input_file}!")
    exit(1)

tokens = re.split("[\n ]+", mlvm_script)
position = 0
todo_labels = {}
labels = {}
output_bytes = []

def append_value(output, value, position, force_half = False):
    assert value <= 0xFFFF
    if value > 0xFF or force_half:
        output.append(value & 0xFF)
        output.append((value >> 8) & 0xFF)
        return position + 2
    else:
        output.append(value & 0xFF)
        return position + 1

def append_placeholder_label(output, label, position):
    todo_labels[position] = label
    output.append(0x00)
    output.append(0x00)
    return position + 2

token_pos = 0
position = 0
offset = 0
commenting = False

while token_pos < len(tokens):
    token = tokens[token_pos]

    if token.startswith("/*"): commenting = True

    if commenting:
        if token.endswith("*/"): commenting = False
        token_pos += 1
        continue

    if token in mlvm.instructions.__dict__:
        opcode = mlvm.instructions.INSTRUCTIONS.index(mlvm.instructions.__dict__[token])
        position = append_value(output_bytes, opcode, position)

    elif token.startswith("."):
        cmd = token.lstrip(".")
        if cmd == "offset":
            token_pos += 1
            offset = position = int(tokens[token_pos], 0) & 0xFFFF

        elif cmd == "seek":
            token_pos += 1
            value = int(tokens[token_pos], 0) & 0xFFFF
            for i in range(value - position):
                position = append_value(output_bytes, 0x00, position)
        
        elif cmd == "set":
            token_pos += 1
            name = tokens[token_pos]
            token_pos += 1
            value = int(tokens[token_pos], 0) & 0xFFFF
            labels[name] = value

    elif token.endswith(":"):
        label = token.rstrip(":")
        labels[label] = position
        
    elif token.startswith("$"):
        label = token.lstrip("$")
        if label not in labels:
            position = append_placeholder_label(output_bytes, label, position)
        else:
            position = append_value(output_bytes, labels[label], position, force_half=True)

    elif len(token):
        position = append_value(output_bytes, int(token, 0), position)
    
    token_pos += 1

for position,label in todo_labels.items():
    output_bytes[position - offset] = labels[label] & 0xFF
    output_bytes[position - offset + 1] = (labels[label] >> 8) & 0xFF

n = 0
for byte in output_bytes:
    if n % 0x10 == 0:
        if n != 0: print("")
        print(f"0x{n:04x}: ", end=" ")

    print(f"0x{byte:02x}", end=" ")
    n += 1

try:
    with open(output_file, "wb") as output_stream:
        output_stream.write(bytes(output_bytes))
except:
    print(f"Failed to open {output_file}!")
    exit(1)
