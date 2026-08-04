from mlvm.const import STACK_START_ADDR
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "LIA",
    long_name="Load Immediate into A",
    description="Loads a 2 byte immediate value into register A.",
    steps=[
        "Fetch the low byte of the immediate value",
        "Fetch the high byte of the immediate value",
        "Combine both bytes and store the result in A",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x00] = LIA = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.scratch | (cpu.bus.data << 8)),
]

doc(
    "LIB",
    long_name="Load Immediate into B",
    description="Loads a 2 byte immediate value into register B.",
    steps=[
        "Fetch the low byte of the immediate value",
        "Fetch the high byte of the immediate value",
        "Combine both bytes and store the result in B",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x01] = LIB = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.scratch | (cpu.bus.data << 8)),
]

doc(
    "LIC",
    long_name="Load Immediate into C",
    description="Loads a 2 byte immediate value into register C.",
    steps=[
        "Fetch the low byte of the immediate value",
        "Fetch the high byte of the immediate value",
        "Combine both bytes and store the result in C",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x02] = LIC = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.scratch | (cpu.bus.data << 8)),
]

doc(
    "LIA8",
    long_name="Load 1 Byte Immediate into A (Zero Extended)",
    description="Loads a 1 byte immediate into A, zero extended to 2 bytes. One byte in ROM, not two.",
    steps=[
        "Fetch the immediate byte",
        "Zero-extend the byte and store the result in A",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x04] = LIA8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data),
]

doc(
    "LIB8",
    long_name="Load 1 Byte Immediate into B (Zero Extended)",
    description="Loads a 1 byte immediate into B, zero extended to 2 bytes.",
    steps=[
        "Fetch the immediate byte",
        "Zero-extend the byte and store the result in B",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x05] = LIB8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data),
]

doc(
    "LIC8",
    long_name="Load 1 Byte Immediate into C (Zero Extended)",
    description="Loads a 1 byte immediate into C, zero extended to 2 bytes.",
    steps=[
        "Fetch the immediate byte",
        "Zero-extend the byte and store the result in C",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x06] = LIC8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data),
]

doc(
    "LIA8S",
    long_name="Load 1 Byte Immediate into A (Sign Extended)",
    description="Loads a 1 byte immediate into A, sign extended to 2 bytes.",
    steps=[
        "Fetch the immediate byte",
        "Sign-extend the byte and store the result in A",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x08] = LIA8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "LIB8S",
    long_name="Load 1 Byte Immediate into B (Sign Extended)",
    description="Loads a 1 byte immediate into B, sign extended to 2 bytes.",
    steps=[
        "Fetch the immediate byte",
        "Sign-extend the byte and store the result in B",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x09] = LIB8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "LIC8S",
    long_name="Load 1 Byte Immediate into C (Sign Extended)",
    description="Loads a 1 byte immediate into C, sign extended to 2 bytes.",
    steps=[
        "Fetch the immediate byte",
        "Sign-extend the byte and store the result in C",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x0A] = LIC8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "SOF",
    long_name="Stack Offset",
    description="Computes a stack-pointer-relative address (STACK_START_ADDR + T + imm16) and stores it in C.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Add STACK_START_ADDR, T, and the offset, and store the result in C",
    ],
    category="Immediate Loads",
)
INSTRUCTIONS[0x0F] = SOF = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_c", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
]
