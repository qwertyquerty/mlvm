from .registry import INSTRUCTIONS
from .loads import *
from .increments import *
from .assignments import *
from .writes import *
from .reads import *
from .operators import *
from .comparisons import *
from .interrupts import *
from .stack import *
from .jumps import *
from .system import *


def instruction_from_name(name):
    return globals()[name] if name in globals() else None


def opcode_from_instruction(instruction):
    return INSTRUCTIONS.index(instruction)


def name_from_opcode(opcode):
    return list(globals().keys())[list(globals().values()).index(INSTRUCTIONS[opcode])]


def name_from_instruction(instruction):
    return list(globals().keys())[list(globals().values()).index(instruction)]
