"""AST node types produced by the parser and consumed by codegen. Plain dataclasses, no behavior."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Expr:
    """RPN token/operand list from infix_to_rpn. Operands are strings (literals, symbols, @name,
    [...] derefs) or marker tuples ("field", base, field), ("call", fn_name, args), etc."""

    rpn: list


@dataclass
class StaticVarDecl:
    name: str
    address: int


@dataclass
class StaticBlockDecl:
    name: str
    address: int


@dataclass
class DataBlockDecl:
    # ROM bytes, addressed by label, not a known address at compile time.
    name: str
    elem_type: str
    values: list
    source_string: str = None


@dataclass
class FunctionDecl:
    name: str
    address: Optional[int]
    local_scope: object  # symbols.LocalScope
    body: list


@dataclass
class BeginMarker:
    # Emits a label.
    pass


@dataclass
class MacroExpansionComment:
    # No runtime effect, marks the name of the outermost macro expanded at this statement.
    name: str


@dataclass
class SymbolTarget:
    name: str


@dataclass
class DerefTarget:
    # set [dest] = value: dest is a literal address or pointer/block var name, width inferred.
    # For a computed multi-token address, dest is None and expr/explicit_type are set instead.
    dest: Optional[str] = None
    expr: Optional[Expr] = None
    explicit_type: Optional[str] = None


@dataclass
class FieldTarget:
    kind: str  # "direct" | "index" | "deref"
    base: str
    field: str
    index_expr: Optional[Expr] = None  # only present when kind == "index"


@dataclass
class SetStmt:
    target: object  # SymbolTarget | DerefTarget | FieldTarget
    value: Expr


@dataclass
class CallStmt:
    fn_name: str
    args: list = field(default_factory=list)  # list[Expr]


@dataclass
class IncrDecrStmt:
    op: str  # "incr" | "decr"
    target: str


@dataclass
class ReturnStmt:
    value: Optional[Expr]
    is_top_level: bool  # top-level return, fallthrough is dead code


@dataclass
class RtiStmt:
    is_top_level: bool


@dataclass
class FrameOpStmt:
    """svi/ldi statement. Evaluates value into register C, then emits SVI/LDI."""

    op: str  # "SVI" or "LDI"
    value: Expr


@dataclass
class IfStmt:
    condition: Expr
    body: list
    else_body: Optional[list] = None


@dataclass
class WhileStmt:
    condition: Expr
    body: list


@dataclass
class AsmToken:
    text: str


@dataclass
class AsmAddressOf:
    # @name inside asm{}, resolved to $mlvc_static_var_name / $mlvc_function_name at codegen time
    name: str


@dataclass
class AsmLabel:
    text: str  # "name:", emitted as is


@dataclass
class AsmDirective:
    text: str  # ".directive args...", emitted as is


@dataclass
class AsmBlock:
    lines: list  # list[AsmToken | AsmAddressOf | AsmLabel | AsmDirective]
