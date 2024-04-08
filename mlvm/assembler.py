"""
MLVM Assembler
"""

import re
from mlvm.instructions import instruction_from_name, opcode_from_instruction
from mlvm.const import *
import sys

VALUE_RE = "(0x[0-9A-Fa-f]+|0b[01]+|-?[0-9]+)"
SYMBOL_RE = "[a-zA-Z\_]+[a-zA-Z0-9\_]*"
WHITESPACE_RE = "[ \n]+"

def append_value(output, value, position, force_half = False):
    # Append a value to the output bytes, if its a half append in little endian
    assert value <= 0xFFFF
    if value > 0xFF or force_half:
        output.append(value & 0xFF)
        output.append((value >> 8) & 0xFF)
        return position + 2
    else:
        output.append(value & 0xFF)
        return position + 1

def append_placeholder_label(output, label, position):
    # Save a label to be filled in later because it has not been defined yet
    todo_labels[position] = label
    output.append(0x00)
    output.append(0x00)
    return position + 2

if __name__ == "__main__":
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

    todo_labels = {} # Dict of labels that will have to be filled on second pass
    labels = {} # Dict of labels to address
    output_bytes = [] # Output bytes for bin file
    token_pos = 0 # Current position in assembly file
    position = 0 # Current position in bytes
    offset = 0 # Start of file offset
    commenting = False # Whether we are currently in a comment

    tokens = re.split("[\n ]+", mlvm_script) # Split input file into tokens

    tokens = [token for token in tokens if token != ""] # Remove empty tokens

    while token_pos < len(tokens):
        token = tokens[token_pos]

        if token.startswith("/*"): commenting = True # Start comment

        if commenting:
            if token.endswith("*/"): commenting = False # End comment
            token_pos += 1
            continue # Ignore everything except for end comment while commenting

        if instruction_from_name(token) is not None: # Instruction
            opcode = opcode_from_instruction(instruction_from_name(token))
            position = append_value(output_bytes, opcode, position)

        elif token.startswith("."): # Directives
            cmd = token.lstrip(".")
            if cmd == "offset":
                # Define the start address of the file, as in where the binary will be placed in the address space of the bus
                token_pos += 1
                offset = position = int(tokens[token_pos], 0) & 0xFFFF

            elif cmd == "seek":
                # Seek to a specific address, fill bytes before then with zeros
                token_pos += 1
                value = int(tokens[token_pos], 0) & 0xFFFF

                if position < value:
                    print("Cannot seek backwards!"); exit(1)

                for i in range(value - position):
                    position = append_value(output_bytes, 0x00, position)
            
            elif cmd == "set":
                # Define a symbol
                token_pos += 1
                name = tokens[token_pos]
                token_pos += 1
                value = int(tokens[token_pos], 0) & 0xFFFF
                labels[name] = value

        elif token.endswith(":"):
            # Labels
            label = token.rstrip(":")
            labels[label] = position
            
        elif token.startswith("$"):
            # Get value of a symbol or label
            label = token.lstrip("$")

            if label not in labels:
                # This label isn't defined yet so add it to a list of labels to be filled in on a second pass later
                position = append_placeholder_label(output_bytes, label, position)
            else:
                position = append_value(output_bytes, labels[label], position, force_half=True)

        elif re.match(VALUE_RE, token):
            # Append raw value
            position = append_value(output_bytes, int(token, 0), position)
        
        elif re.match(WHITESPACE_RE, token):
            ...

        else:
            print(f"Syntax error: {token}"); exit(1)

        token_pos += 1

    # Do a second pass to fill in labels we skipped earlier
    for position,label in todo_labels.items():
        output_bytes[position - offset] = labels[label] & 0xFF
        output_bytes[position - offset + 1] = (labels[label] >> 8) & 0xFF

    # Hex output
    n = 0
    for byte in output_bytes:
        if n % 0x10 == 0:
            if n != 0: print("")
            print(f"0x{n:04x}: ", end=" ")

        print(f"0x{byte:02x}", end=" ")
        n += 1

    # Write bytes to output file
    try:
        with open(output_file, "wb") as output_stream:
            output_stream.write(bytes(output_bytes))
    except:
        print(f"Failed to open {output_file}!")
        exit(1)
