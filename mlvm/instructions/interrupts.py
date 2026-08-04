from .registry import INSTRUCTIONS
from .docs import doc

# Byte layout of a saved interrupt frame: (P, A, B, C, D, S, T), matching the tuple
# MLVMProcessor.enter_interrupt snapshots (see processor.py). S is 1 byte, everything else 2 bytes,
# little-endian, in field order.
_FRAME_FIELD_WIDTHS = (2, 2, 2, 2, 2, 1, 2)  # P, A, B, C, D, S, T
_FRAME_SIZE = sum(_FRAME_FIELD_WIDTHS)  # 13


def _frame_to_bytes(frame):
    out = []
    for value, width in zip(frame, _FRAME_FIELD_WIDTHS):
        out.extend((value >> (8 * i)) & 0xFF for i in range(width))
    return out


def _frame_from_bytes(data):
    values = []
    i = 0
    for width in _FRAME_FIELD_WIDTHS:
        value = 0
        for b in range(width):
            value |= data[i + b] << (8 * b)
        values.append(value)
        i += width
    return tuple(values)


def _capture_frame_byte(cpu, index):
    # Mutating a list in place isn't expressible as a single lambda expression - this is the one
    # bit of real logic pulled out into a helper the step lambdas below call into.
    cpu.frame_scratch[index] = cpu.bus.data
    if index == _FRAME_SIZE - 1:
        cpu.interrupt_stack[-1] = _frame_from_bytes(cpu.frame_scratch)


doc(
    "SVI",
    long_name="Save Interrupt Frame",
    description=(
        "Writes the pending interrupt-return frame (P, A, B, C, D, S, T - what a plain RTI would "
        "restore) to memory starting at the address in C, 1 byte per cycle. This is the primitive "
        "a preemptive scheduler needs: on interrupt entry A/B/C/D/T are already live with the "
        "interrupted process's values, so only P needs saving out of a register."
    ),
    steps=[
        "Write the low byte of P to [C+0]",
        "Write the high byte of P to [C+1]",
        "Write the low byte of A to [C+2]",
        "Write the high byte of A to [C+3]",
        "Write the low byte of B to [C+4]",
        "Write the high byte of B to [C+5]",
        "Write the low byte of C to [C+6]",
        "Write the high byte of C to [C+7]",
        "Write the low byte of D to [C+8]",
        "Write the high byte of D to [C+9]",
        "Write S to [C+10]",
        "Write the low byte of T to [C+11]",
        "Write the high byte of T to [C+12]",
        "Delay one cycle so the last write commits",
    ],
    category="Interrupts",
)
INSTRUCTIONS[0xE0] = SVI = [
    (
        lambda cpu, index=index: cpu.bus.write(
            (cpu.reg_c + index) & 0xFFFF, _frame_to_bytes(cpu.interrupt_stack[-1])[index]
        )
    )
    for index in range(_FRAME_SIZE)
] + [None]

doc(
    "LDI",
    long_name="Load Interrupt Frame",
    description=(
        "Reads a frame previously written by SVI back from memory at the address in C, replacing "
        "the pending interrupt frame, so the RTI that follows resumes into whatever was saved there "
        "instead of the process that was actually interrupted."
    ),
    steps=[
        "Reset the frame buffer and read the low byte of P from [C+0]",
        "Store the low byte of P and read the high byte of P from [C+1]",
        "Store the high byte of P and read the low byte of A from [C+2]",
        "Store the low byte of A and read the high byte of A from [C+3]",
        "Store the high byte of A and read the low byte of B from [C+4]",
        "Store the low byte of B and read the high byte of B from [C+5]",
        "Store the high byte of B and read the low byte of C from [C+6]",
        "Store the low byte of C and read the high byte of C from [C+7]",
        "Store the high byte of C and read the low byte of D from [C+8]",
        "Store the low byte of D and read the high byte of D from [C+9]",
        "Store the high byte of D and read S from [C+10]",
        "Store S and read the low byte of T from [C+11]",
        "Store the low byte of T and read the high byte of T from [C+12]",
        "Store the high byte of T and replace the pending interrupt frame with the collected bytes",
    ],
    category="Interrupts",
)
INSTRUCTIONS[0xE1] = LDI = (
    [lambda cpu: (setattr(cpu, "frame_scratch", [0] * _FRAME_SIZE), cpu.bus.read(cpu.reg_c))]
    + [
        (
            lambda cpu, index=index: (
                _capture_frame_byte(cpu, index),
                cpu.bus.read((cpu.reg_c + index + 1) & 0xFFFF),
            )
        )
        for index in range(_FRAME_SIZE - 1)
    ]
    + [lambda cpu: _capture_frame_byte(cpu, _FRAME_SIZE - 1)]
)

doc(
    "INT",
    long_name="Software Interrupt",
    description=(
        "Raises IRQ <imm8> immediately, exactly as if a peripheral had called bus.irq() this cycle - "
        "same deferral rules apply (blocked by CLI, STATUS_IN_IRQ, or STATUS_IN_NMI). Lets software "
        "voluntarily trigger an IRQ handler instead of only reacting to real hardware timing."
    ),
    steps=[
        "Fetch the immediate IRQ id",
        "Raise that IRQ",
    ],
    category="Interrupts",
)
INSTRUCTIONS[0xEB] = INT = [
    lambda cpu: (
        setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF),
        cpu.bus.read(cpu.reg_p),
    ),
    lambda cpu: cpu.bus.irq(cpu.bus.data),
]
