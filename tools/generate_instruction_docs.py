import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mlvm.instructions import INSTRUCTIONS, name_from_opcode
from mlvm.instructions.docs import INSTRUCTION_DOCS

DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "instructions.md"

CATEGORY_ORDER = [
    "Immediate Loads",
    "Memory Reads",
    "Memory Writes",
    "Register Assignment",
    "Increment and Decrement",
    "Arithmetic and Bitwise Operators",
    "Comparisons",
    "Jumps",
    "Stack and Subroutines",
    "Interrupts",
    "System Control",
]


def slugify(text):
    slug = text.lower()
    slug = "".join(c for c in slug if c.isalnum() or c in " -")
    return slug.replace(" ", "-")


def anchor_for(name):
    return slugify(f"{name}")


def cell_text(opcode):
    instruction = INSTRUCTIONS[opcode]
    if instruction is None:
        return ""
    name = name_from_opcode(opcode)
    doc = INSTRUCTION_DOCS[name]
    cycles = len(instruction)
    return f"[**{name}**](#{anchor_for(name)})<br>{cycles}c"


def build_table():
    header = "| | " + " | ".join(f"`0x_{col:X}`" for col in range(16)) + " |"
    separator = "|" + "---|" * 17

    rows = [header, separator]
    for row in range(16):
        cells = [cell_text(row * 16 + col) for col in range(16)]
        rows.append(f"| `0x{row:X}_` | " + " | ".join(cells) + " |")

    return "\n".join(rows)


def instructions_by_category():
    by_category = {category: [] for category in CATEGORY_ORDER}
    for opcode, instruction in enumerate(INSTRUCTIONS):
        if instruction is None:
            continue
        name = name_from_opcode(opcode)
        doc = INSTRUCTION_DOCS[name]
        by_category[doc.category].append((opcode, name, doc))
    for entries in by_category.values():
        entries.sort(key=lambda entry: entry[0])
    return by_category


def build_toc(by_category):
    lines = []
    for category in CATEGORY_ORDER:
        if not by_category[category]:
            continue
        lines.append(f"- [{category}](#{slugify(category)})")
    return "\n".join(lines)


def build_sections(by_category):
    sections = []
    for category in CATEGORY_ORDER:
        entries = by_category[category]
        if not entries:
            continue
        sections.append(f"## {category}")
        sections.append("")
        for opcode, name, doc in entries:
            cycles = len(INSTRUCTIONS[opcode])
            sections.append(f"### {name}")
            sections.append(f"> Name: {doc.long_name}  ")
            sections.append(f"> Opcode: `0x{opcode:02X}`  ")
            sections.append(f"> Cycles: {cycles}")
            sections.append("")
            sections.append(doc.description)
            sections.append("")
            for i,step in enumerate(doc.steps):
                sections.append(f"{i+1}. {step}")
            sections.append("")
    return "\n".join(sections)


def build_document():
    by_category = instructions_by_category()
    parts = [
        "# MLVM Instruction Set Architecture",
        "",
        build_toc(by_category),
        "",
        build_table(),
        "",
        build_sections(by_category),
    ]
    return "\n".join(parts).rstrip() + "\n"


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_document(), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
