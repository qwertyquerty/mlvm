from mlvm.const import ERR_STACK_OVERFLOW, ERR_STACK_UNDERFLOW, STACK_START_ADDR, STACK_POINTER_MAX
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "SRT",
    long_name="Jump to Subroutine",
    description="Pushes the return address and jumps to the address in C.",
    steps=[
        "Push the low byte of the return address P onto the stack, checking for overflow",
        "Push the high byte of the return address, checking for overflow",
        "Jump to C",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE2] = SRT = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_p", (cpu.reg_c - 1) & 0xFFFF),
]

doc(
    "SIA",
    long_name="Jump to Subroutine if A",
    description="Pushes the return address and jumps to the address in C, only if A is nonzero.",
    steps=[
        "If A is nonzero, push the low byte of the return address, checking for overflow",
        "If A is nonzero, push the high byte of the return address, checking for overflow",
        "If A is nonzero, jump to C",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE3] = SIA = [
    lambda cpu: (
        (
            ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
            cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
            setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        )
        if cpu.reg_a
        else ...
    ),
    lambda cpu: (
        (
            ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
            cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
            setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        )
        if cpu.reg_a
        else ...
    ),
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_c - 1) & 0xFFFF) if cpu.reg_a else ...),
]

doc(
    "SIB",
    long_name="Jump to Subroutine if B",
    description="Pushes the return address and jumps to the address in C, only if B is nonzero.",
    steps=[
        "If B is nonzero, push the low byte of the return address, checking for overflow",
        "If B is nonzero, push the high byte of the return address, checking for overflow",
        "If B is nonzero, jump to C",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE4] = SIB = [
    lambda cpu: (
        (
            ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
            cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
            setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        )
        if cpu.reg_b
        else ...
    ),
    lambda cpu: (
        (
            ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
            cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
            setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        )
        if cpu.reg_b
        else ...
    ),
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_c - 1) & 0xFFFF) if cpu.reg_b else ...),
]

doc(
    "SIC",
    long_name="Jump to Subroutine if C",
    description="Pushes the return address and jumps to the address in C, only if C is nonzero.",
    steps=[
        "If C is nonzero, push the low byte of the return address, checking for overflow",
        "If C is nonzero, push the high byte of the return address, checking for overflow",
        "If C is nonzero, jump to C",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE5] = SIC = [
    lambda cpu: (
        (
            ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
            cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
            setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        )
        if cpu.reg_c
        else ...
    ),
    lambda cpu: (
        (
            ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
            cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
            setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        )
        if cpu.reg_c
        else ...
    ),
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_c - 1) & 0xFFFF) if cpu.reg_c else ...),
]

doc(
    "SRI",
    long_name="Jump to Subroutine, Immediate",
    description="Pushes the return address and jumps to an immediate address.",
    steps=[
        "Fetch the low byte of the target address",
        "Fetch the high byte of the target address",
        "Combine the address and push the low byte of the return address, checking for overflow",
        "Push the high byte of the return address, checking for overflow",
        "Jump to the target address",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE6] = SRI = [
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
        setattr(cpu, "reg_c", cpu.scratch | (cpu.bus.data << 8)),
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: setattr(cpu, "reg_p", (cpu.reg_c - 1) & 0xFFFF),
]

doc(
    "RET",
    long_name="Return from Subroutine",
    description="Pops the return address pushed by a subroutine call and resumes there.",
    steps=[
        "Check for underflow, pop the low byte of the return address",
        "Check for underflow, pop the high byte of the return address",
        "Combine both bytes and set P to the return address",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE7] = RET = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_p", (cpu.scratch << 8) | cpu.bus.data),
]

doc(
    "RTI",
    long_name="Return from Interrupt",
    description=(
        "Restores P, A, B, C, D, S, and T from the pending interrupt frame and resumes execution "
        "there. See SVI/LDI for how that frame can be swapped before this runs."
    ),
    steps=["Restore the saved frame and resume execution"],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE8] = RTI = [lambda cpu: cpu.exit_interrupt()]

doc(
    "PSHI",
    long_name="Push Immediate",
    description=(
        "Pushes a 2 byte immediate value directly onto the stack without touching any register. "
        "One cycle cheaper than the equivalent LIx <imm>; PSHx pair, since the second byte's fetch "
        "overlaps the first byte's stack write."
    ),
    steps=[
        "Fetch the low byte of the immediate value",
        "Fetch the high byte of the immediate value",
        "Push the low byte, checking for overflow, and stash the high byte",
        "Push the high byte, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xE9] = PSHI = [
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
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.scratch & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
        setattr(cpu, "scratch", cpu.bus.data),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.scratch & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHI8",
    long_name="Push Immediate Byte",
    description="Pushes a 1 byte immediate value directly onto the stack. One byte in ROM, not two.",
    steps=[
        "Fetch the immediate byte",
        "Push the byte, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xEA] = PSHI8 = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.bus.data & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHA",
    long_name="Push A",
    description="Pushes A onto the stack.",
    steps=[
        "Push the low byte of A, checking for overflow",
        "Push the high byte of A, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF0] = PSHA = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_a & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_a >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHB",
    long_name="Push B",
    description="Pushes B onto the stack.",
    steps=[
        "Push the low byte of B, checking for overflow",
        "Push the high byte of B, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF1] = PSHB = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_b & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_b >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHC",
    long_name="Push C",
    description="Pushes C onto the stack.",
    steps=[
        "Push the low byte of C, checking for overflow",
        "Push the high byte of C, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF2] = PSHC = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_c & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_c >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHD",
    long_name="Push D",
    description="Pushes D onto the stack.",
    steps=[
        "Push the low byte of D, checking for overflow",
        "Push the high byte of D, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF3] = PSHD = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_d & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_d >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PULA",
    long_name="Pull into A",
    description="Pops the top of the stack (2 bytes) into A.",
    steps=[
        "Check for underflow, pop the low byte",
        "Check for underflow, pop the high byte",
        "Combine both bytes and store the result in A",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF4] = PULA = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_a", (cpu.scratch << 8) | cpu.bus.data),
]

doc(
    "PULB",
    long_name="Pull into B",
    description="Pops the top of the stack (2 bytes) into B.",
    steps=[
        "Check for underflow, pop the low byte",
        "Check for underflow, pop the high byte",
        "Combine both bytes and store the result in B",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF5] = PULB = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_b", (cpu.scratch << 8) | cpu.bus.data),
]

doc(
    "PULC",
    long_name="Pull into C",
    description="Pops the top of the stack (2 bytes) into C.",
    steps=[
        "Check for underflow, pop the low byte",
        "Check for underflow, pop the high byte",
        "Combine both bytes and store the result in C",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF6] = PULC = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_c", (cpu.scratch << 8) | cpu.bus.data),
]

doc(
    "PULD",
    long_name="Pull into D",
    description="Pops the top of the stack (2 bytes) into D.",
    steps=[
        "Check for underflow, pop the low byte",
        "Check for underflow, pop the high byte",
        "Combine both bytes and store the result in D",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF7] = PULD = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: (
        setattr(cpu, "scratch", cpu.bus.data),
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_d", (cpu.scratch << 8) | cpu.bus.data),
]

doc(
    "PSHA8",
    long_name="Push Byte of A",
    description="Pushes the low byte of A onto the stack.",
    steps=[
        "Push the low byte of A, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF8] = PSHA8 = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_a & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHB8",
    long_name="Push Byte of B",
    description="Pushes the low byte of B onto the stack.",
    steps=[
        "Push the low byte of B, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xF9] = PSHB8 = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_b & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHC8",
    long_name="Push Byte of C",
    description="Pushes the low byte of C onto the stack.",
    steps=[
        "Push the low byte of C, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xFA] = PSHC8 = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_c & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PSHD8",
    long_name="Push Byte of D",
    description="Pushes the low byte of D onto the stack.",
    steps=[
        "Push the low byte of D, checking for overflow",
        "Delay one cycle so the write commits",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xFB] = PSHD8 = [
    lambda cpu: (
        ((print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...),
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_d & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF),
    ),
    None,
]

doc(
    "PULA8",
    long_name="Pull Byte into A",
    description="Pops the top of the stack (1 byte) into A, zero extended.",
    steps=[
        "Check for underflow, pop the byte",
        "Zero-extend the byte and store the result in A",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xFC] = PULA8 = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data),
]

doc(
    "PULB8",
    long_name="Pull Byte into B",
    description="Pops the top of the stack (1 byte) into B, zero extended.",
    steps=[
        "Check for underflow, pop the byte",
        "Zero-extend the byte and store the result in B",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xFD] = PULB8 = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data),
]

doc(
    "PULC8",
    long_name="Pull Byte into C",
    description="Pops the top of the stack (1 byte) into C, zero extended.",
    steps=[
        "Check for underflow, pop the byte",
        "Zero-extend the byte and store the result in C",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xFE] = PULC8 = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data),
]

doc(
    "PULD8",
    long_name="Pull Byte into D",
    description="Pops the top of the stack (1 byte) into D, zero extended.",
    steps=[
        "Check for underflow, pop the byte",
        "Zero-extend the byte and store the result in D",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xFF] = PULD8 = [
    lambda cpu: (
        ((print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...),
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t),
    ),
    lambda cpu: setattr(cpu, "reg_d", cpu.bus.data),
]

doc(
    "PSHN",
    long_name="Bulk Reserve",
    description="T += imm16, without touching memory. Bulk equivalent of imm16/2 PSHes.",
    steps=[
        "Fetch the low byte of the count",
        "Fetch the high byte of the count",
        "Check for overflow and add the count to T",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xEE] = PSHN = [
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
        (
            (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW))
            if cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8)) > STACK_POINTER_MAX
            else ...
        ),
        setattr(cpu, "reg_t", (cpu.reg_t + (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
    ),
]

doc(
    "PULN",
    long_name="Bulk Release",
    description="T -= imm16, without touching memory. Bulk equivalent of imm16/2 PULs.",
    steps=[
        "Fetch the low byte of the count",
        "Fetch the high byte of the count",
        "Check for underflow and subtract the count from T",
    ],
    category="Stack and Subroutines",
)
INSTRUCTIONS[0xEF] = PULN = [
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
        (
            (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW))
            if (cpu.scratch | (cpu.bus.data << 8)) > cpu.reg_t
            else ...
        ),
        setattr(cpu, "reg_t", (cpu.reg_t - (cpu.scratch | (cpu.bus.data << 8))) & 0xFFFF),
    ),
]
