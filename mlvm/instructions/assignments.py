from .registry import INSTRUCTIONS
from .docs import doc

doc(
    "SAB",
    long_name="Set A from B",
    description="Copies B into A.",
    steps=["Set A to the value of B."],
    category="Register Assignment",
)
INSTRUCTIONS[0x90] = SAB = [lambda cpu: setattr(cpu, "reg_a", cpu.reg_b)]

doc(
    "SAC",
    long_name="Set A from C",
    description="Copies C into A.",
    steps=["Set A to the value of C."],
    category="Register Assignment",
)
INSTRUCTIONS[0x91] = SAC = [lambda cpu: setattr(cpu, "reg_a", cpu.reg_c)]

doc(
    "SAS",
    long_name="Set A from S",
    description="Copies the status register S into A.",
    steps=["Set A to the value of S."],
    category="Register Assignment",
)
INSTRUCTIONS[0x92] = SAS = [lambda cpu: setattr(cpu, "reg_a", cpu.reg_s)]

doc(
    "SBA",
    long_name="Set B from A",
    description="Copies A into B.",
    steps=["Set B to the value of A."],
    category="Register Assignment",
)
INSTRUCTIONS[0x93] = SBA = [lambda cpu: setattr(cpu, "reg_b", cpu.reg_a)]

doc(
    "SBC",
    long_name="Set B from C",
    description="Copies C into B.",
    steps=["Set B to the value of C."],
    category="Register Assignment",
)
INSTRUCTIONS[0x94] = SBC = [lambda cpu: setattr(cpu, "reg_b", cpu.reg_c)]

doc(
    "SCA",
    long_name="Set C from A",
    description="Copies A into C.",
    steps=["Set C to the value of A."],
    category="Register Assignment",
)
INSTRUCTIONS[0x95] = SCA = [lambda cpu: setattr(cpu, "reg_c", cpu.reg_a)]

doc(
    "SCB",
    long_name="Set C from B",
    description="Copies B into C.",
    steps=["Set C to the value of B."],
    category="Register Assignment",
)
INSTRUCTIONS[0x96] = SCB = [lambda cpu: setattr(cpu, "reg_c", cpu.reg_b)]

doc(
    "SDC",
    long_name="Set D from C",
    description="Copies C into D.",
    steps=["Set D to the value of C."],
    category="Register Assignment",
)
INSTRUCTIONS[0x97] = SDC = [lambda cpu: setattr(cpu, "reg_d", cpu.reg_c)]

doc(
    "SAD",
    long_name="Set A from D",
    description="Copies D into A.",
    steps=["Set A to the value of D."],
    category="Register Assignment",
)
INSTRUCTIONS[0x98] = SAD = [lambda cpu: setattr(cpu, "reg_a", cpu.reg_d)]

doc(
    "SBD",
    long_name="Set B from D",
    description="Copies D into B.",
    steps=["Set B to the value of D."],
    category="Register Assignment",
)
INSTRUCTIONS[0x99] = SBD = [lambda cpu: setattr(cpu, "reg_b", cpu.reg_d)]

doc(
    "SCD",
    long_name="Set C from D",
    description="Copies D into C.",
    steps=["Set C to the value of D."],
    category="Register Assignment",
)
INSTRUCTIONS[0x9A] = SCD = [lambda cpu: setattr(cpu, "reg_c", cpu.reg_d)]
