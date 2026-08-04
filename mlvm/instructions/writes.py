from mlvm.const import STACK_START_ADDR
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "WRA",
    long_name="Write A",
    description="Writes 2 bytes of A to the address in C.",
    steps=[
        "Write the low byte of A to address C",
        "Write the high byte of A to address C+1",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x30] = WRA = [
    lambda cpu: cpu.bus.write(cpu.reg_c, cpu.reg_a & 0xFF),
    lambda cpu: cpu.bus.write((cpu.reg_c + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "WRB",
    long_name="Write B",
    description="Writes 2 bytes of B to the address in C.",
    steps=[
        "Write the low byte of B to address C",
        "Write the high byte of B to address C+1",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x31] = WRB = [
    lambda cpu: cpu.bus.write(cpu.reg_c, cpu.reg_b & 0xFF),
    lambda cpu: cpu.bus.write((cpu.reg_c + 1) & 0xFFFF, (cpu.reg_b >> 8) & 0xFF),
    None,
]

doc(
    "WRC",
    long_name="Write C",
    description="Writes 2 bytes of C to the address in C.",
    steps=[
        "Write the low byte of C to address C",
        "Write the high byte of C to address C+1",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x32] = WRC = [
    lambda cpu: cpu.bus.write(cpu.reg_c, cpu.reg_c & 0xFF),
    lambda cpu: cpu.bus.write((cpu.reg_c + 1) & 0xFFFF, (cpu.reg_c >> 8) & 0xFF),
    None,
]

doc(
    "WRA8",
    long_name="Write Byte of A",
    description="Writes the low 1 byte of A to the address in C.",
    steps=[
        "Write the low byte of A to address C",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x34] = WRA8 = [
    lambda cpu: cpu.bus.write(cpu.reg_c, cpu.reg_a & 0xFF),
    None,
]

doc(
    "WRB8",
    long_name="Write Byte of B",
    description="Writes the low 1 byte of B to the address in C.",
    steps=[
        "Write the low byte of B to address C",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x35] = WRB8 = [
    lambda cpu: cpu.bus.write(cpu.reg_c, cpu.reg_b & 0xFF),
    None,
]

doc(
    "WRC8",
    long_name="Write Byte of C",
    description="Writes the low 1 byte of C to the address in C.",
    steps=[
        "Write the low byte of C to address C",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x36] = WRC8 = [
    lambda cpu: cpu.bus.write(cpu.reg_c, cpu.reg_c & 0xFF),
    None,
]

doc(
    "WSA",
    long_name="Write Stack-Relative A",
    description="Writes 2 bytes of A to (STACK_START_ADDR + T + imm16).",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and write the low byte of A there",
        "Write the high byte of A",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x40] = WSA = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "WSB",
    long_name="Write Stack-Relative B",
    description="Writes 2 bytes of B to (STACK_START_ADDR + T + imm16).",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and write the low byte of B there",
        "Write the high byte of B",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x41] = WSB = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_b & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_b >> 8) & 0xFF),
    None,
]

doc(
    "WSC",
    long_name="Write Stack-Relative C",
    description="Writes 2 bytes of C to (STACK_START_ADDR + T + imm16).",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and write the low byte of C there",
        "Write the high byte of C",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x42] = WSC = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_c & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_c >> 8) & 0xFF),
    None,
]

doc(
    "WSA8",
    long_name="Write Stack-Relative Byte of A",
    description="Writes the low 1 byte of A to (STACK_START_ADDR + T + imm16).",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and write the low byte of A there",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x44] = WSA8 = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    None,
]

doc(
    "WSB8",
    long_name="Write Stack-Relative Byte of B",
    description="Writes the low 1 byte of B to (STACK_START_ADDR + T + imm16).",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and write the low byte of B there",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x45] = WSB8 = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_b & 0xFF),
    ),
    None,
]

doc(
    "WSC8",
    long_name="Write Stack-Relative Byte of C",
    description="Writes the low 1 byte of C to (STACK_START_ADDR + T + imm16).",
    steps=[
        "Fetch the low byte of the offset immediate",
        "Fetch the high byte of the offset immediate",
        "Compute the stack-relative address and write the low byte of C there",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x46] = WSC8 = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_c & 0xFF),
    ),
    None,
]

doc(
    "WIA",
    long_name="Write Immediate-Address A",
    description="Writes 2 bytes of A to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and write the low byte of A there",
        "Write the high byte of A",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x60] = WIA = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_a >> 8) & 0xFF),
    None,
]

doc(
    "WIB",
    long_name="Write Immediate-Address B",
    description="Writes 2 bytes of B to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and write the low byte of B there",
        "Write the high byte of B",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x61] = WIB = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_b & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_b >> 8) & 0xFF),
    None,
]

doc(
    "WIC",
    long_name="Write Immediate-Address C",
    description="Writes 2 bytes of C to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and write the low byte of C there",
        "Write the high byte of C",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x62] = WIC = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_c & 0xFF),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, (cpu.reg_c >> 8) & 0xFF),
    None,
]

doc(
    "WIA8",
    long_name="Write Immediate-Address Byte of A",
    description="Writes the low 1 byte of A to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and write the low byte of A there",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x64] = WIA8 = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_a & 0xFF),
    ),
    None,
]

doc(
    "WIB8",
    long_name="Write Immediate-Address Byte of B",
    description="Writes the low 1 byte of B to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and write the low byte of B there",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x65] = WIB8 = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_b & 0xFF),
    ),
    None,
]

doc(
    "WIC8",
    long_name="Write Immediate-Address Byte of C",
    description="Writes the low 1 byte of C to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and write the low byte of C there",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x66] = WIC8 = [
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
        cpu.bus.write(cpu.scratch, cpu.reg_c & 0xFF),
    ),
    None,
]

doc(
    "WII",
    long_name="Write Immediate Value to Immediate Address",
    description="Writes a 2 byte immediate value to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and fetch the low byte of the immediate value",
        "Write the low byte of the value to the address",
        "Fetch the high byte of the immediate value",
        "Write the high byte of the value to address+1",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x6E] = WII = [
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
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: cpu.bus.write(cpu.scratch, cpu.bus.data & 0xFF),
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: cpu.bus.write((cpu.scratch + 1) & 0xFFFF, cpu.bus.data & 0xFF),
    None,
]

doc(
    "WII8",
    long_name="Write Immediate Byte to Immediate Address",
    description="Writes a 1 byte immediate value to an immediate absolute address.",
    steps=[
        "Fetch the low byte of the address",
        "Fetch the high byte of the address",
        "Combine the address and fetch the immediate value byte",
        "Write the value byte to the address",
        "Delay one cycle so the write commits",
    ],
    category="Memory Writes",
)
INSTRUCTIONS[0x6F] = WII8 = [
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
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: cpu.bus.write(cpu.scratch, cpu.bus.data & 0xFF),
    None,
]
