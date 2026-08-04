from mlvm.const import STACK_START_ADDR
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "INA",
    long_name="Increment A",
    description="Increments A by 1, wrapping at 0xFFFF.",
    steps=["Increment A."],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA0] = INA = [lambda cpu: setattr(cpu, "reg_a", (cpu.reg_a + 1) & 0xFFFF)]

doc(
    "INB",
    long_name="Increment B",
    description="Increments B by 1, wrapping at 0xFFFF.",
    steps=["Increment B."],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA1] = INB = [lambda cpu: setattr(cpu, "reg_b", (cpu.reg_b + 1) & 0xFFFF)]

doc(
    "INC",
    long_name="Increment C",
    description="Increments C by 1, wrapping at 0xFFFF.",
    steps=["Increment C."],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA2] = INC = [lambda cpu: setattr(cpu, "reg_c", (cpu.reg_c + 1) & 0xFFFF)]

doc(
    "DEA",
    long_name="Decrement A",
    description="Decrements A by 1, wrapping at 0xFFFF.",
    steps=["Decrement A."],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA3] = DEA = [lambda cpu: setattr(cpu, "reg_a", (cpu.reg_a - 1) & 0xFFFF)]

doc(
    "DEB",
    long_name="Decrement B",
    description="Decrements B by 1, wrapping at 0xFFFF.",
    steps=["Decrement B."],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA4] = DEB = [lambda cpu: setattr(cpu, "reg_b", (cpu.reg_b - 1) & 0xFFFF)]

doc(
    "DEC",
    long_name="Decrement C",
    description="Decrements C by 1, wrapping at 0xFFFF.",
    steps=["Decrement C."],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA5] = DEC = [lambda cpu: setattr(cpu, "reg_c", (cpu.reg_c - 1) & 0xFFFF)]

doc(
    "INS",
    long_name="Increment Stack-Relative",
    description="Increments the 2 byte value at (STACK_START_ADDR + T + imm16) by 1.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the low byte of the value there",
        "Store the low byte in A and read the high byte of the value",
        "Combine and increment the value, then write the low byte back",
        "Write the high byte back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA6] = INS = [
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
    lambda cpu: (
        setattr(cpu, "reg_a", ((cpu.reg_a | (cpu.bus.data << 8)) + 1) & 0xFFFF),
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "INS8",
    long_name="Increment Stack-Relative Byte",
    description="Increments the 1 byte value at (STACK_START_ADDR + T + imm16) by 1.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Increment the value and write it back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA7] = INS8 = [
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
    lambda cpu: cpu.bus.write(cpu.scratch, (cpu.bus.data + 1) & 0xFF),
    None,
]

doc(
    "INI",
    long_name="Increment Immediate-Address",
    description="Increments the 2 byte value at an immediate absolute address by 1.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the low byte of the value there",
        "Store the low byte in A and read the high byte of the value",
        "Combine and increment the value, then write the low byte back",
        "Write the high byte back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA8] = INI = [
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
    lambda cpu: (
        setattr(cpu, "reg_a", ((cpu.reg_a | (cpu.bus.data << 8)) + 1) & 0xFFFF),
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "INI8",
    long_name="Increment Immediate-Address Byte",
    description="Increments the 1 byte value at an immediate absolute address by 1.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Increment the value and write it back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xA9] = INI8 = [
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
    lambda cpu: cpu.bus.write(cpu.scratch, (cpu.bus.data + 1) & 0xFF),
    None,
]

doc(
    "DES",
    long_name="Decrement Stack-Relative",
    description="Decrements the 2 byte value at (STACK_START_ADDR + T + imm16) by 1.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the low byte of the value there",
        "Store the low byte in A and read the high byte of the value",
        "Combine and decrement the value, then write the low byte back",
        "Write the high byte back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xAA] = DES = [
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
    lambda cpu: (
        setattr(cpu, "reg_a", ((cpu.reg_a | (cpu.bus.data << 8)) - 1) & 0xFFFF),
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "DES8",
    long_name="Decrement Stack-Relative Byte",
    description="Decrements the 1 byte value at (STACK_START_ADDR + T + imm16) by 1.",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and read the value byte there",
        "Decrement the value and write it back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xAB] = DES8 = [
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
    lambda cpu: cpu.bus.write(cpu.scratch, (cpu.bus.data - 1) & 0xFF),
    None,
]

doc(
    "DEI",
    long_name="Decrement Immediate-Address",
    description="Decrements the 2 byte value at an immediate absolute address by 1.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the low byte of the value there",
        "Store the low byte in A and read the high byte of the value",
        "Combine and decrement the value, then write the low byte back",
        "Write the high byte back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xAC] = DEI = [
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
    lambda cpu: (
        setattr(cpu, "reg_a", ((cpu.reg_a | (cpu.bus.data << 8)) - 1) & 0xFFFF),
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "DEI8",
    long_name="Decrement Immediate-Address Byte",
    description="Decrements the 1 byte value at an immediate absolute address by 1.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and read the value byte there",
        "Decrement the value and write it back",
        "Delay one cycle so the write commits",
    ],
    category="Increment and Decrement",
)
INSTRUCTIONS[0xAD] = DEI8 = [
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
    lambda cpu: cpu.bus.write(cpu.scratch, (cpu.bus.data - 1) & 0xFF),
    None,
]
