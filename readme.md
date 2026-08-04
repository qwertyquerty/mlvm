# MLVM
## Modular Limited Virtual Machine

A custom instruction set, assembler, compiler, and virtual machine in Python.

This is a hobby project for educational purposes.

## Documentation

- [`mlvc.md`](mlvc.md): the MLVC language reference, syntax and features
- [`instructions.md`](instructions.md): the full CPU instruction set

## Common Nomenclature

- `bus`: The data, address, and intent lines connected to every device, as well as a clock
    - `write`: Putting an address to write to on the data lines, a value on the data lines, and setting the intent line to write
    - `read`: Putting an address to read from on the address lines, and setting the intent line to read
    - `respond`: Putting a value on the data lines without changing the intent line or address lines
- `device`: Any component connected to the bus like RAM, ROM, the processor, or peripherals
- `peripheral`: A device that largely encapsulates its entire operation, and only interacts with other devices via a few registers and bus responds
- `register`: Small units of memory inside the processor which are used by instructions
    - `A/B/C registers`: 16 bit registers used in most operations, where A and B are generally the operands, C usually contains the result, and C additionally doubles as the address register for memory reads/writes and jumps
    - `program counter`: The 16 bit P register, which keeps track of the current execution position, where the processor will load the next instruction from
    - `stack pointer`: The 16 bit T register, which keeps track of the current height of the stack plus 1, the next stack position to be written to when the stack is pushed to
    - `status register`: The 8 bit S register, stores different status flags from the processor (interrupt enable, and whether an NMI/IRQ is currently being serviced)
- `type`: Every MLVC variable must declare a type, one of `u8`, `u16`, `i8`, or `i16`; the type controls how many bytes are allocated and whether reads from memory are zero- or sign-extended into the 16 bit registers
- `cycle`: One full clock cycle including a negative and then positive edge
- `instruction`: Procedures defined under `mlvm/instructions/` which define steps of CPU operations based on opcodes in the ROM

## Default Address Layout

By default, address space is laid out as shown below

- `0x0000 ... 0x5FFF`: Random Access Memory
    - `0x0000 ... 0x0FFF`: Stack
    - `0x1000 ... 0x5FFF`: Program Memory
- `0x6000 ... 0x7FFF`: Peripherals
    - `0x6000 ... 0x607F`: Video Peripheral Registers
    - `0x6080 ... 0x60FF`: Gamepad Peripheral Registers
    - `0x6100 ... 0x617F`: Timer Peripheral Registers
- `0x8000 ... 0xFFFF`: Read Only Memory
    - `0x8000 ... 0x????`: Binary Executable

## Project Setup

> It is heavily recommended to install [pypy](https://www.pypy.org/) or the virtual machine will likely not be able to maintain a very fast clock speed

`pip install -r requirements.txt`

`pypy -m pip install -r requirements.txt`

## Compiling/Running Code

You can compile, assemble, and run any `.mlvc` file, for example Lavender OS at `lvos/lvos.mlvc`.

Compiling the code: `python -m mlvm.compiler lvos/lvos.mlvc lvos/lvos.mlvs`

Assembling and generating the ROM: `python -m mlvm.assembler lvos/lvos.mlvs lvos/lvos.bin`

Loading and running the ROM: `pypy -m mlvm lvos/lvos.bin`

### Build and run in one step

`pypy -m tools.build_and_run lvos/lvos.mlvc`
