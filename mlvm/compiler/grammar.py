import re

# Virtual registers for inverse
INVERSE_REGISTERS = {"A": "X", "B": "Y", "C": "Z"}

# Order of operations, higher precedence later in the list
EXPRESSION_OPERATOR_PRECEDENCE = (
    "&&",
    "==",
    "!=",
    ">=",
    "<=",
    ">",
    "<",
    "|",
    "^",
    "&",
    "<<",
    ">>",
    "+",
    "-",
    "*",
    "/",
    "%",
    "~",
    "u-",
)

# Mapping operators to their instruction
EXPRESSION_OPERATOR_INSTRUCTION_MAP = {
    "==": "CMP",
    "!=": "NEQ",
    ">=": "GTE",
    "<=": "LTE",
    ">": "GTC",
    "<": "LTC",
    "|": "IOR",
    "^": "XOR",
    "&": "AND",
    "<<": "LSS",
    ">>": "RSS",
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "~": "NOT",
    "u-": "NEG",
    "&&": "ANL",
    "%": "MOD",
    "/": "DIV",
}

# Unary operators: each pops exactly one RPN operand instead of two
UNARY_OPERATORS = ("~", "u-")

# List of all operators
OPERATORS = (
    "/*",
    "*/",
    "==",
    "!=",
    ">=",
    "<=",
    "=",
    ">>",
    "<<",
    ">",
    "<",
    "{",
    "}",
    "[",
    "]",
    '"',
    "'",
    "+",
    "-",
    "*",
    "(",
    ")",
    "&&",
    "&",
    "|",
    "^",
    "~",
    "#",
    "@",
    "!",
    "?",
    ";",
    "%",
    "/",
    ",",
)

# Variable/expression data types
TYPE_U8 = "u8"
TYPE_U16 = "u16"
TYPE_I8 = "i8"
TYPE_I16 = "i16"
TYPE_KEYWORDS = (TYPE_U8, TYPE_U16, TYPE_I8, TYPE_I16)

# Size in bytes of each type
TYPE_SIZES = {TYPE_U8: 1, TYPE_I8: 1, TYPE_U16: 2, TYPE_I16: 2}

# RD{reg} suffix for reading each type
TYPE_READ_SUFFIX = {TYPE_U8: "8", TYPE_I8: "8S", TYPE_U16: "", TYPE_I16: ""}

# WR{reg} suffix for writing each type
TYPE_WRITE_SUFFIX = {TYPE_U8: "8", TYPE_I8: "8", TYPE_U16: "", TYPE_I16: ""}


# Pointer types are written as [type] (e.g. [u16]), but stored internally as type*
def is_pointer_type(var_type):
    return var_type.endswith("*")


# Array types (both top-level `array` blocks and struct array fields) are stored internally as type[count]
_ARRAY_TYPE_RE = re.compile(r"^(.+)\[(\d+)\]$")


def is_block_type(var_type):
    return _ARRAY_TYPE_RE.match(var_type) is not None


def pointee_type(var_type):
    return var_type[:-1]


def block_element_type(var_type):
    return _ARRAY_TYPE_RE.match(var_type).group(1)


def block_element_count(var_type):
    return int(_ARRAY_TYPE_RE.match(var_type).group(2))


def var_size(var_type):
    return 2 if is_pointer_type(var_type) else TYPE_SIZES[var_type]


def var_read_suffix(var_type):
    return "" if is_pointer_type(var_type) else TYPE_READ_SUFFIX[var_type]


def var_write_suffix(var_type):
    return "" if is_pointer_type(var_type) else TYPE_WRITE_SUFFIX[var_type]


# List of reserved keywords
KEYWORDS = [
    "fn",
    "define",
    "macro",
    "include",
    "var",
    "array",
    "data",
    "struct",
    "set",
    "if",
    "else",
    "while",
    "asm",
    "begin",
    "return",
    "rti",
    "call",
    "incr",
    "decr",
    "svi",
    "ldi",
] + list(TYPE_KEYWORDS)

VALUE_RE = r"(0x[0-9A-Fa-f]+|0b[01]+|-?[0-9]+)"
SYMBOL_RE = r"[a-zA-Z\_]+[a-zA-Z0-9\_]*"
WHITESPACE_RE = r"[ \n]+"

# Escape set for string/char literals
_ESCAPES = {"n": "\n", "r": "\r", "0": "\0", "\\": "\\", '"': '"', "'": "'"}


def unescape_literal(raw_inner):
    out = []
    i = 0
    while i < len(raw_inner):
        c = raw_inner[i]
        if c == "\\" and i + 1 < len(raw_inner) and raw_inner[i + 1] in _ESCAPES:
            out.append(_ESCAPES[raw_inner[i + 1]])
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)
