# CrossPy6502 Documentation
## Introduction

Welcome to CrossPy6502, an experimental and platform-independent assembly language cross-compiler for the 6502 microprocessor, written in Python. It directly translates assembly code into machine code, simplifying the process of assembling 6502 code across all major operating systems.

I originally started the project to improve my Python skills and to figure out for myself how a compiler can work and, of course, to learn more about the 6502. My initial goal was to translate my own assembly source code into machine code and run it on native hardware. Since others might also find this project useful, I decided to share it here. 

**Please note: This compiler is still under development and may not be fully optimized or bug-free. Your feedback and bug reports are greatly appreciated!**

## Compiling source code

The source code includes an example assembly file with a hardcoded BASIC stub for the C64 that executes the assembly code. This file can be directly translated into an executable PRG file for the C64:
```bash
python3 main.py example.asm example.prg
```
The output file `example.prg` can then be executed within an C64 emulator or native hardware, for example with help of an SD2IEC adapter.

Of course, the compiler is not limited to the C64. It can also be used to compile assembly code into plain binary files, such as for an EEPROM:
```bash
python3 main.py example.asm example.bin
```

## Syntax
CrossPy6502 supports the standard 6502 assembly language syntax with some exceptions: 

1. The implemented directives `.org`, `.const` `.byte`, `.word`, `.res` and `.text` start with a `.` instead of a `!`.
2. Labels must be on separate lines and always followed by a colon, for example, `label_name:`.
3. Source files can be included using the `.include "<path>filename"` directive. CrossPy6502 supports nested `.include` directives.
4. Constants are defined by `.const NAME <value>` and must not have the same names as labels.
    
**Documentation is currently unavailable. Please refer to the included example files for a better understanding of the syntax.**
