from mlvm.const import STATUS_HALT, STATUS_CLI
from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "HLT",
    long_name="Halt",
    description="Stops processing.",
    steps=["Set the halt status bit"],
    category="System Control",
)
INSTRUCTIONS[0x80] = HLT = [lambda cpu: (print("HALT"), setattr(cpu, "reg_s", cpu.reg_s | STATUS_HALT))]

doc(
    "CLI",
    long_name="Disable Interrupts",
    description="Sets the CLI status bit, blocking IRQs and NMIs.",
    steps=["Set the CLI status bit"],
    category="System Control",
)
INSTRUCTIONS[0x81] = CLI = [lambda cpu: setattr(cpu, "reg_s", cpu.reg_s | STATUS_CLI)]

doc(
    "STI",
    long_name="Enable Interrupts",
    description="Clears the CLI status bit, allowing IRQs and NMIs.",
    steps=["Clear the CLI status bit"],
    category="System Control",
)
INSTRUCTIONS[0x82] = STI = [lambda cpu: setattr(cpu, "reg_s", cpu.reg_s & ~STATUS_CLI)]
