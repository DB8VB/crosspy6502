# Experimental 6502 Assembly to Machine Code Compiler
# by DB8VB
# v0.1a
# 2024-12-29
# License: BSD 2-Clause License

import  sys
from    tokenize import *
from    parser import *
from    memory import *


def main(argv):
    if len(argv) != 3:
        print("CrossPy6502 v0.1a - Experimental 6502 Assembly Compiler by DB8VB")
        print("Usage: python main.py <input_file> <output_file>")
        print("Example for C64 executable: python main.py test.asm test.prg")
        sys.exit(1)

    input_file  = argv[1]
    output_file = argv[2]

    # Tokenize: Each line is a list containing the first word and the rest of the line
    with open(input_file, 'rt') as fp:
        tokens = tokenize(fp)

    # Get the memory offset from the first source code line (.org) - if no .org directive given, default: 0x0000
    offset          = get_memory_offset(tokens)

    # Get constants and replace them with corresponding values in the source code
    constants       = get_constants(tokens)
    tokens          = replace_constants(tokens, constants)

    # Get the labels from source code
    labels          = get_labels(tokens)

    # Get the offsets of the labels from source code
    label_offsets   = get_label_offsets(tokens, offset, labels)

    # Replace labels with addresses
    tokens = labels_to_adresses(tokens, label_offsets)

    # Replace labels with relative addresses (for branches, e.g. BNE, BEQ, etc.)
    tokens = compute_relative_relative_addresses(tokens, offset, label_offsets)

    # Parse the tokens and generate the op codes
    op_codes = parse(tokens)

    # Write the op codes to the output file
    with open(output_file, 'wb') as file:
        for i in range(len(op_codes)):
            file.write(op_codes[i].to_bytes(1, byteorder='big'))

if __name__ == "__main__":
    main(sys.argv)