from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "CMP",
    long_name="Equals",
    description="C = 1 if A == B, else 0.",
    steps=["Compare A and B for equality and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC0] = CMP = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a == cpu.reg_b))]

doc(
    "GTE",
    long_name="Unsigned Greater Than or Equal",
    description="C = 1 if A >= B (unsigned), else 0.",
    steps=["Compare A and B as unsigned values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC1] = GTE = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a >= cpu.reg_b))]

doc(
    "LTE",
    long_name="Unsigned Less Than or Equal",
    description="C = 1 if A <= B (unsigned), else 0.",
    steps=["Compare A and B as unsigned values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC2] = LTE = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a <= cpu.reg_b))]

doc(
    "GTC",
    long_name="Unsigned Greater Than",
    description="C = 1 if A > B (unsigned), else 0.",
    steps=["Compare A and B as unsigned values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC3] = GTC = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a > cpu.reg_b))]

doc(
    "LTC",
    long_name="Unsigned Less Than",
    description="C = 1 if A < B (unsigned), else 0.",
    steps=["Compare A and B as unsigned values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC4] = LTC = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a < cpu.reg_b))]

doc(
    "SGE",
    long_name="Signed Greater Than or Equal",
    description="C = 1 if A >= B, comparing both as two's complement signed values, else 0.",
    steps=["Compare A and B as signed values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC5] = SGE = [
    lambda cpu: setattr(
        cpu,
        "reg_c",
        int(
            (cpu.reg_a - 0x10000 if cpu.reg_a & 0x8000 else cpu.reg_a)
            >= (cpu.reg_b - 0x10000 if cpu.reg_b & 0x8000 else cpu.reg_b)
        ),
    )
]

doc(
    "SLE",
    long_name="Signed Less Than or Equal",
    description="C = 1 if A <= B, comparing both as two's complement signed values, else 0.",
    steps=["Compare A and B as signed values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC6] = SLE = [
    lambda cpu: setattr(
        cpu,
        "reg_c",
        int(
            (cpu.reg_a - 0x10000 if cpu.reg_a & 0x8000 else cpu.reg_a)
            <= (cpu.reg_b - 0x10000 if cpu.reg_b & 0x8000 else cpu.reg_b)
        ),
    )
]

doc(
    "SGT",
    long_name="Signed Greater Than",
    description="C = 1 if A > B, comparing both as two's complement signed values, else 0.",
    steps=["Compare A and B as signed values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC7] = SGT = [
    lambda cpu: setattr(
        cpu,
        "reg_c",
        int(
            (cpu.reg_a - 0x10000 if cpu.reg_a & 0x8000 else cpu.reg_a)
            > (cpu.reg_b - 0x10000 if cpu.reg_b & 0x8000 else cpu.reg_b)
        ),
    )
]

doc(
    "SLT",
    long_name="Signed Less Than",
    description="C = 1 if A < B, comparing both as two's complement signed values, else 0.",
    steps=["Compare A and B as signed values and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC8] = SLT = [
    lambda cpu: setattr(
        cpu,
        "reg_c",
        int(
            (cpu.reg_a - 0x10000 if cpu.reg_a & 0x8000 else cpu.reg_a)
            < (cpu.reg_b - 0x10000 if cpu.reg_b & 0x8000 else cpu.reg_b)
        ),
    )
]

doc(
    "NEQ",
    long_name="Not Equal",
    description="C = 1 if A != B, else 0.",
    steps=["Compare A and B for inequality and store the result in C"],
    category="Comparisons",
)
INSTRUCTIONS[0xC9] = NEQ = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a != cpu.reg_b))]
