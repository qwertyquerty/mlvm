"""Compiler entry point. Lexes, parses to an AST, then runs codegen to produce .mlvs text."""

from .symbols import SymbolTable
from .parser import Parser
from .codegen import Codegen
from .errors import MlvcSyntaxError, MlvcMemoryError


class CompilerStateMachine:
    def __init__(self, mlvc_filename, cwd):
        self.mlvc_filename = mlvc_filename
        self.cwd = cwd

    def generate(self):
        symbols = SymbolTable()
        parser = Parser(symbols, self.cwd)
        codegen = Codegen(symbols)

        try:
            program = parser.parse_program(self.mlvc_filename)
            return codegen.generate(program)
        except MlvcSyntaxError as e:
            file = e.file or self.mlvc_filename
            line = e.line if e.line is not None else "?"
            print(f"SYNTAX ERROR IN {file} ON LINE {line}: {e.message}")
            exit(1)
        except MlvcMemoryError as e:
            print(f"MEMORY ERROR: {e.message}")
            exit(2)


__all__ = ["CompilerStateMachine"]
