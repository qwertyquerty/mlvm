from mlvm.const import STATUS_CARRY
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "AND",
    long_name="Bitwise AND",
    description="C = A & B.",
    steps=["Set C to A bitwise AND B"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB0] = AND = [lambda cpu: setattr(cpu, "reg_c", cpu.reg_a & cpu.reg_b)]

doc(
    "IOR",
    long_name="Bitwise OR",
    description="C = A | B.",
    steps=["Set C to A bitwise OR B"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB1] = IOR = [lambda cpu: setattr(cpu, "reg_c", cpu.reg_a | cpu.reg_b)]

doc(
    "XOR",
    long_name="Bitwise XOR",
    description="C = A ^ B.",
    steps=["Set C to A bitwise XOR B"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB2] = XOR = [lambda cpu: setattr(cpu, "reg_c", cpu.reg_a ^ cpu.reg_b)]

doc(
    "NOT",
    long_name="Bitwise NOT",
    description="C = ~A. B is not used.",
    steps=["Set C to the bitwise complement of A"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB3] = NOT = [lambda cpu: setattr(cpu, "reg_c", ~cpu.reg_a & 0xFFFF)]

doc(
    "ADD",
    long_name="Addition",
    description="C = A + B. Sets the carry status bit if the result overflowed 2 bytes.",
    steps=["Add A and B into C, updating the carry flag"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB4] = ADD = [
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a + cpu.reg_b) & 0xFFFF),
        setattr(
            cpu,
            "reg_s",
            ((cpu.reg_s | STATUS_CARRY) if (cpu.reg_a + cpu.reg_b) > 0xFFFF else (cpu.reg_s & ~STATUS_CARRY)),
        ),
    )
]

doc(
    "SUB",
    long_name="Subtraction",
    description="C = A - B, computed via two's complement. Sets the carry status bit if the result overflowed.",
    steps=["Subtract B from A into C, updating the carry flag"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB5] = SUB = [
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a + (~cpu.reg_b + 1) & 0xFFFF) & 0xFFFF),
        setattr(
            cpu,
            "reg_s",
            (
                (cpu.reg_s | STATUS_CARRY)
                if (cpu.reg_a + (~cpu.reg_b + 1) & 0xFFFF) > 0xFFFF
                else (cpu.reg_s & ~STATUS_CARRY)
            ),
        ),
    )
]

doc(
    "MUL",
    long_name="Multiplication",
    description="C = (A * B), truncated to 2 bytes. There is no wide/high-half result.",
    steps=["Multiply A by B, truncate to 2 bytes, and store the result in C"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB6] = MUL = [lambda cpu: setattr(cpu, "reg_c", (cpu.reg_a * cpu.reg_b) & 0xFFFF)]

doc(
    "RSS",
    long_name="Right Shift",
    description="C = A >> B.",
    steps=["Shift A right by B bits and store the result in C"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB7] = RSS = [lambda cpu: setattr(cpu, "reg_c", (cpu.reg_a >> cpu.reg_b) & 0xFFFF)]

doc(
    "LSS",
    long_name="Left Shift",
    description="C = A << B, truncated to 2 bytes.",
    steps=["Shift A left by B bits and store the result in C"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB8] = LSS = [lambda cpu: setattr(cpu, "reg_c", (cpu.reg_a << cpu.reg_b) & 0xFFFF)]

doc(
    "ANL",
    long_name="Logical AND",
    description="C = 1 if both A and B are nonzero, else 0.",
    steps=["Set C to the logical AND of A and B"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xB9] = ANL = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a and cpu.reg_b))]

doc(
    "MOD",
    long_name="Modulo",
    description="C = A % B.",
    steps=["Set C to A modulo B"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xBA] = MOD = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a % cpu.reg_b))]

doc(
    "DIV",
    long_name="Integer Division",
    description="C = A // B.",
    steps=["Set C to A divided by B, rounded down"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xBB] = DIV = [lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a // cpu.reg_b))]

doc(
    "NEG",
    long_name="Negate",
    description="C = -A, two's complement. B is not used.",
    steps=["Set C to the two's complement negation of A"],
    category="Arithmetic and Bitwise Operators",
)
INSTRUCTIONS[0xBC] = NEG = [lambda cpu: setattr(cpu, "reg_c", (-cpu.reg_a) & 0xFFFF)]
