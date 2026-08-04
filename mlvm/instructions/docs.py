from dataclasses import dataclass
from typing import List

INSTRUCTION_DOCS = {}


@dataclass
class InstructionDoc:
    name: str
    long_name: str
    description: str
    steps: List[str]
    category: str


def doc(name, long_name, description, steps, category):
    INSTRUCTION_DOCS[name] = InstructionDoc(name, long_name, description, steps, category)
