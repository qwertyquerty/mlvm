from mlvm.const import STACK_START_ADDR
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "RDA",
    long_name="Read into A",
    description="Reads 2 bytes at the address in C into A.",
    steps=[
        "Read the low byte at address C",
        "Read the high byte at address C+1",
        "Combine both bytes and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x10] = RDA = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: (setattr(cpu, "scratch", cpu.bus.data), cpu.bus.read((cpu.reg_c + 1) & 0xFFFF)),
    lambda cpu: setattr(cpu, "reg_a", cpu.scratch | (cpu.bus.data << 8)),
]

doc(
    "RDB",
    long_name="Read into B",
    description="Reads 2 bytes at the address in C into B.",
    steps=[
        "Read the low byte at address C",
        "Read the high byte at address C+1",
        "Combine both bytes and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x11] = RDB = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: (setattr(cpu, "scratch", cpu.bus.data), cpu.bus.read((cpu.reg_c + 1) & 0xFFFF)),
    lambda cpu: setattr(cpu, "reg_b", cpu.scratch | (cpu.bus.data << 8)),
]

doc(
    "RDC",
    long_name="Read into C",
    description="Reads 2 bytes at the address in C into C.",
    steps=[
        "Read the low byte at address C",
        "Read the high byte at address C+1",
        "Combine both bytes and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x12] = RDC = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: (setattr(cpu, "scratch", cpu.bus.data), cpu.bus.read((cpu.reg_c + 1) & 0xFFFF)),
    lambda cpu: setattr(cpu, "reg_c", cpu.scratch | (cpu.bus.data << 8)),
]

doc(
    "RDA8",
    long_name="Read Byte into A (Zero Extended)",
    description="Reads 1 byte at the address in C into A, zero extended.",
    steps=[
        "Read the byte at address C",
        "Zero-extend the byte and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x14] = RDA8 = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data),
]

doc(
    "RDB8",
    long_name="Read Byte into B (Zero Extended)",
    description="Reads 1 byte at the address in C into B, zero extended.",
    steps=[
        "Read the byte at address C",
        "Zero-extend the byte and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x15] = RDB8 = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data),
]

doc(
    "RDC8",
    long_name="Read Byte into C (Zero Extended)",
    description="Reads 1 byte at the address in C into C, zero extended.",
    steps=[
        "Read the byte at address C",
        "Zero-extend the byte and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x16] = RDC8 = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data),
]

doc(
    "RDA8S",
    long_name="Read Byte into A (Sign Extended)",
    description="Reads 1 byte at the address in C into A, sign extended.",
    steps=[
        "Read the byte at address C",
        "Sign-extend the byte and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x18] = RDA8S = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RDB8S",
    long_name="Read Byte into B (Sign Extended)",
    description="Reads 1 byte at the address in C into B, sign extended.",
    steps=[
        "Read the byte at address C",
        "Sign-extend the byte and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x19] = RDB8S = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RDC8S",
    long_name="Read Byte into C (Sign Extended)",
    description="Reads 1 byte at the address in C into C, sign extended.",
    steps=[
        "Read the byte at address C",
        "Sign-extend the byte and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x1A] = RDC8S = [
    lambda cpu: cpu.bus.read(cpu.reg_c),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RSA",
    long_name="Read Stack-Relative into A",
    description="Reads 2 bytes at (STACK_START_ADDR + T + imm16) into A.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the low byte of the value there",
        "Store the low byte in A and read the high byte of the value",
        "Combine the high byte into A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x20] = RSA = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: (
        setattr(cpu, "reg_a", cpu.bus.data),
        cpu.bus.read((cpu.scratch + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_a | (cpu.bus.data << 8)),
]

doc(
    "RSB",
    long_name="Read Stack-Relative into B",
    description="Reads 2 bytes at (STACK_START_ADDR + T + imm16) into B.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the low byte of the value there",
        "Store the low byte in B and read the high byte of the value",
        "Combine the high byte into B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x21] = RSB = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: (
        setattr(cpu, "reg_b", cpu.bus.data),
        cpu.bus.read((cpu.scratch + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.reg_b | (cpu.bus.data << 8)),
]

doc(
    "RSC",
    long_name="Read Stack-Relative into C",
    description="Reads 2 bytes at (STACK_START_ADDR + T + imm16) into C.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the low byte of the value there",
        "Store the low byte in C and read the high byte of the value",
        "Combine the high byte into C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x22] = RSC = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: (
        setattr(cpu, "reg_c", cpu.bus.data),
        cpu.bus.read((cpu.scratch + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_c | (cpu.bus.data << 8)),
]

doc(
    "RSA8",
    long_name="Read Stack-Relative Byte into A (Zero Extended)",
    description="Reads 1 byte at (STACK_START_ADDR + T + imm16) into A, zero extended.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Zero-extend the byte and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x24] = RSA8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data),
]

doc(
    "RSB8",
    long_name="Read Stack-Relative Byte into B (Zero Extended)",
    description="Reads 1 byte at (STACK_START_ADDR + T + imm16) into B, zero extended.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Zero-extend the byte and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x25] = RSB8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data),
]

doc(
    "RSC8",
    long_name="Read Stack-Relative Byte into C (Zero Extended)",
    description="Reads 1 byte at (STACK_START_ADDR + T + imm16) into C, zero extended.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Zero-extend the byte and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x26] = RSC8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data),
]

doc(
    "RSA8S",
    long_name="Read Stack-Relative Byte into A (Sign Extended)",
    description="Reads 1 byte at (STACK_START_ADDR + T + imm16) into A, sign extended.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Sign-extend the byte and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x28] = RSA8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RSB8S",
    long_name="Read Stack-Relative Byte into B (Sign Extended)",
    description="Reads 1 byte at (STACK_START_ADDR + T + imm16) into B, sign extended.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Sign-extend the byte and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x29] = RSB8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RSC8S",
    long_name="Read Stack-Relative Byte into C (Sign Extended)",
    description="Reads 1 byte at (STACK_START_ADDR + T + imm16) into C, sign extended.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Sign-extend the byte and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x2A] = RSC8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", (STACK_START_ADDR + cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RIA",
    long_name="Read Immediate-Address into A",
    description="Reads 2 bytes at an immediate absolute address into A.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the low byte of the value there",
        "Store the low byte in A and read the high byte of the value",
        "Combine the high byte into A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x50] = RIA = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: (
        setattr(cpu, "reg_a", cpu.bus.data),
        cpu.bus.read((cpu.scratch + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_a | (cpu.bus.data << 8)),
]

doc(
    "RIB",
    long_name="Read Immediate-Address into B",
    description="Reads 2 bytes at an immediate absolute address into B.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the low byte of the value there",
        "Store the low byte in B and read the high byte of the value",
        "Combine the high byte into B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x51] = RIB = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: (
        setattr(cpu, "reg_b", cpu.bus.data),
        cpu.bus.read((cpu.scratch + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.reg_b | (cpu.bus.data << 8)),
]

doc(
    "RIC",
    long_name="Read Immediate-Address into C",
    description="Reads 2 bytes at an immediate absolute address into C.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the low byte of the value there",
        "Store the low byte in C and read the high byte of the value",
        "Combine the high byte into C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x52] = RIC = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: (
        setattr(cpu, "reg_c", cpu.bus.data),
        cpu.bus.read((cpu.scratch + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_c | (cpu.bus.data << 8)),
]

doc(
    "RIA8",
    long_name="Read Immediate-Address Byte into A (Zero Extended)",
    description="Reads 1 byte at an immediate absolute address into A, zero extended.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Zero-extend the byte and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x54] = RIA8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data),
]

doc(
    "RIB8",
    long_name="Read Immediate-Address Byte into B (Zero Extended)",
    description="Reads 1 byte at an immediate absolute address into B, zero extended.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Zero-extend the byte and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x55] = RIB8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data),
]

doc(
    "RIC8",
    long_name="Read Immediate-Address Byte into C (Zero Extended)",
    description="Reads 1 byte at an immediate absolute address into C, zero extended.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Zero-extend the byte and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x56] = RIC8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data),
]

doc(
    "RIA8S",
    long_name="Read Immediate-Address Byte into A (Sign Extended)",
    description="Reads 1 byte at an immediate absolute address into A, sign extended.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Sign-extend the byte and store the result in A",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x58] = RIA8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RIB8S",
    long_name="Read Immediate-Address Byte into B (Sign Extended)",
    description="Reads 1 byte at an immediate absolute address into B, sign extended.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Sign-extend the byte and store the result in B",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x59] = RIB8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]

doc(
    "RIC8S",
    long_name="Read Immediate-Address Byte into C (Sign Extended)",
    description="Reads 1 byte at an immediate absolute address into C, sign extended.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Sign-extend the byte and store the result in C",
    ],
    category="Memory Reads",
)
INSTRUCTIONS[0x5A] = RIC8S = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.scratch | (cpu.bus.data << 8)),
        cpu.bus.read(cpu.scratch),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data | 0xFF00 if cpu.bus.data & 0x80 else cpu.bus.data),
]
