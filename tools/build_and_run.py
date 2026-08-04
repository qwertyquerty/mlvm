import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mlvm.compiler import CompilerStateMachine
from mlvm.assembler import assemble
from mlvm.vm import build_machine, run


def compile_to_mlvs(mlvc_path):
    csm = CompilerStateMachine(str(mlvc_path), os.getcwd())
    mlvs_source = csm.generate()

    mlvs_path = mlvc_path.with_suffix(".mlvs")
    mlvs_path.write_text(mlvs_source, encoding="utf-8")
    return mlvs_path


def assemble_to_bin(mlvs_path):
    mlvs_source = mlvs_path.read_text(encoding="utf-8")
    rom_bytes = assemble(mlvs_source)

    bin_path = mlvs_path.with_suffix(".bin")
    bin_path.write_bytes(rom_bytes)
    return bin_path


def main():
    if len(sys.argv) < 2:
        print("You must specify an input .mlvc or .mlvs file!")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    suffix = input_path.suffix.lower()

    if suffix == ".mlvc":
        mlvs_path = compile_to_mlvs(input_path)
    elif suffix == ".mlvs":
        mlvs_path = input_path
    else:
        print(f"Unrecognized file extension {suffix!r}, expected .mlvc or .mlvs!")
        sys.exit(1)

    bin_path = assemble_to_bin(mlvs_path)

    machine = build_machine(str(bin_path))
    run(machine)


if __name__ == "__main__":
    main()
