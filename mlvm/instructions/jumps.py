from mlvm.const import STATUS_CARRY
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "JMP",
    long_name="Jump",
    description="Jumps to the address in C.",
    steps=["Set P to C minus 1, so the next fetch lands on C"],
    category="Jumps",
)
INSTRUCTIONS[0xD0] = JMP = [lambda cpu: setattr(cpu, "reg_p", (cpu.reg_c - 1) & 0xFFFF)]

doc(
    "JIA",
    long_name="Jump if A",
    description="Jumps to the address in C if A is nonzero.",
    steps=["Jump to C if A is nonzero"],
    category="Jumps",
)
INSTRUCTIONS[0xD1] = JIA = [lambda cpu: JMP[0](cpu) if cpu.reg_a else ...]

doc(
    "JIB",
    long_name="Jump if B",
    description="Jumps to the address in C if B is nonzero.",
    steps=["Jump to C if B is nonzero"],
    category="Jumps",
)
INSTRUCTIONS[0xD2] = JIB = [lambda cpu: JMP[0](cpu) if cpu.reg_b else ...]

doc(
    "JIC",
    long_name="Jump if C",
    description="Jumps to the address in C if C is nonzero.",
    steps=["Jump to C if C is nonzero"],
    category="Jumps",
)
INSTRUCTIONS[0xD3] = JIC = [lambda cpu: JMP[0](cpu) if cpu.reg_c else ...]

doc(
    "JIX",
    long_name="Jump if not A",
    description="Jumps to the address in C if A is zero.",
    steps=["Jump to C if A is zero"],
    category="Jumps",
)
INSTRUCTIONS[0xD4] = JIX = [lambda cpu: JMP[0](cpu) if not cpu.reg_a else ...]

doc(
    "JIY",
    long_name="Jump if not B",
    description="Jumps to the address in C if B is zero.",
    steps=["Jump to C if B is zero"],
    category="Jumps",
)
INSTRUCTIONS[0xD5] = JIY = [lambda cpu: JMP[0](cpu) if not cpu.reg_b else ...]

doc(
    "JIZ",
    long_name="Jump if not C",
    description="Jumps to the address in C if C is zero.",
    steps=["Jump to C if C is zero"],
    category="Jumps",
)
INSTRUCTIONS[0xD6] = JIZ = [lambda cpu: JMP[0](cpu) if not cpu.reg_c else ...]

doc(
    "JSC",
    long_name="Jump if Carry",
    description="Jumps to the address in C if the carry status bit is set.",
    steps=["Jump to C if the carry flag is set"],
    category="Jumps",
)
INSTRUCTIONS[0xD7] = JSC = [lambda cpu: JMP[0](cpu) if (cpu.reg_s & STATUS_CARRY) else ...]

doc(
    "JMI",
    long_name="Jump Immediate",
    description=(
        "Jumps to an immediate address. The address is staged in the internal scratch byte, not a "
        "general register, so it never disturbs A/B/C."
    ),
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "Set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xD8] = JMI = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF),
]

doc(
    "JAI",
    long_name="Jump Immediate if A",
    description="Jumps to an immediate address if A is nonzero.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "If A is nonzero, set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xD9] = JAI = [
    JMI[0],
    JMI[1],
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF) if cpu.reg_a else ...),
]

doc(
    "JBI",
    long_name="Jump Immediate if B",
    description="Jumps to an immediate address if B is nonzero.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "If B is nonzero, set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xDA] = JBI = [
    JMI[0],
    JMI[1],
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF) if cpu.reg_b else ...),
]

doc(
    "JCI",
    long_name="Jump Immediate if C",
    description="Jumps to an immediate address if C is nonzero.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "If C is nonzero, set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xDB] = JCI = [
    JMI[0],
    JMI[1],
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF) if cpu.reg_c else ...),
]

doc(
    "JXI",
    long_name="Jump Immediate if not A",
    description="Jumps to an immediate address if A is zero.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "If A is zero, set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xDC] = JXI = [
    JMI[0],
    JMI[1],
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF) if not cpu.reg_a else ...),
]

doc(
    "JYI",
    long_name="Jump Immediate if not B",
    description="Jumps to an immediate address if B is zero.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "If B is zero, set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xDD] = JYI = [
    JMI[0],
    JMI[1],
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF) if not cpu.reg_b else ...),
]

doc(
    "JZI",
    long_name="Jump Immediate if not C",
    description="Jumps to an immediate address if C is zero.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "If C is zero, set P to the target address minus 1",
    ],
    category="Jumps",
)
INSTRUCTIONS[0xDE] = JZI = [
    JMI[0],
    JMI[1],
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.scratch | (cpu.bus.data << 8)) - 1) & 0xFFFF) if not cpu.reg_c else ...),
]
