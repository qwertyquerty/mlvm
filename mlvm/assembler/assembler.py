import re

from mlvm.const import ROM_SIZE
from mlvm.instructions import instruction_from_name, opcode_from_instruction

VALUE_RE = r"(0x[0-9A-Fa-f]+|0b[01]+|-?[0-9]+)"
SYMBOL_RE = r"[a-zA-Z\_]+[a-zA-Z0-9\_]*"
WHITESPACE_RE = r"[ \n]+"
STRING_RE = r'"(?:[^"\\\n]|\\.)*"'
CHAR_RE = r"'(?:[^'\\\n]|\\.)*'"

_COMMENT_OR_QUOTED_RE = re.compile(r"/\*.*?\*/|" + STRING_RE + "|" + CHAR_RE, re.DOTALL)

# Same escape set as the compiler's grammar.unescape_literal
_ESCAPES = {"n": "\n", "r": "\r", "0": "\0", "\\": "\\", '"': '"', "'": "'"}


def _unescape(raw_inner):
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


def _extract_quoted_spans(text):
    # Replaces each quoted string with a placeholder so the whitespace-splitting tokenizer can't
    # fragment one with embedded spaces. Returns substituted text plus placeholder -> span map.
    spans = {}

    def replace(m):
        if m.group(0).startswith("/*"):
            return m.group(0)  # a comment, leave as-is
        placeholder = f"\x00STR{len(spans)}\x00"
        spans[placeholder] = m.group(0)
        return placeholder

    return _COMMENT_OR_QUOTED_RE.sub(replace, text), spans


def _char_literal_value(token):
    inner = _unescape(token[1:-1])
    if len(inner) != 1:
        print(f"Syntax error: malformed char literal {token}")
        exit(1)
    return ord(inner)


# Byte width in ROM of each immediate operand, in order, for instructions not using the default
# 2 bytes. Anything not listed defaults to 2 bytes (an address or full 16-bit value).
NARROW_IMMEDIATE_WIDTHS = {
    "LIA8": [1],
    "LIB8": [1],
    "LIC8": [1],
    "LIA8S": [1],
    "LIB8S": [1],
    "LIC8S": [1],
    "PSHI8": [1],
    "INT": [1],
    "WII8": [2, 1],
}


class Assembler:
    """Assembles MLVM assembly source into a ROM binary, two passes: the first walks the token
    stream emitting bytes and directives, the second backfills forward-referenced labels."""

    def __init__(self):
        self.tokens = []
        self.token_pos = 0
        self.position = 0
        self.offset = 0
        self.commenting = False
        self.todo_labels = {}
        self.labels = {}
        self.seekstack = []
        self.output = None
        self.pending_widths = []

        self.directives = {
            "offset": self._directive_offset,
            "seek": self._directive_seek,
            "seekpush": self._directive_seekpush,
            "seekpop": self._directive_seekpop,
            "set": self._directive_set,
            "byte": self._directive_byte,
            "word": self._directive_word,
        }

    def assemble(self, source_text):
        substituted, spans = _extract_quoted_spans(source_text)
        self.tokens = [spans.get(t, t) for t in re.split("[\n ]+", substituted) if t != ""]
        self.token_pos = 0
        self.position = 0
        self.offset = 0
        self.commenting = False
        self.todo_labels = {}
        self.labels = {}
        self.seekstack = []
        self.output = [None for _ in range(ROM_SIZE)]
        self.pending_widths = []

        while self.token_pos < len(self.tokens):
            self._process_token(self.tokens[self.token_pos])
            self.token_pos += 1

        # Second pass to fill in labels that weren't yet defined when they were referenced
        for position, label in self.todo_labels.items():
            self.output[position - self.offset] = self.labels[label] & 0xFF
            self.output[position - self.offset + 1] = (self.labels[label] >> 8) & 0xFF

        return bytes(0x00 if b is None else b for b in self.output)

    def _process_token(self, token):
        if token.startswith("/*"):
            self.commenting = True

        if self.commenting:  # ignore everything except the end of the comment
            if token.endswith("*/"):
                self.commenting = False
            return

        instruction = instruction_from_name(token)
        if instruction is not None:
            self._append_value(opcode_from_instruction(instruction))
            self.pending_widths = list(NARROW_IMMEDIATE_WIDTHS.get(token, []))

        elif token.startswith("."):  # directive, unrecognized ones silently ignored
            directive = self.directives.get(token.lstrip("."))
            if directive is not None:
                directive()

        elif token.endswith(":"):  # label
            self.labels[token.rstrip(":")] = self.position

        elif token.startswith("$"):  # reference to the value of a symbol or label
            self._next_immediate_width()  # labels are a full address, but still consume the slot
            label = token.lstrip("$")
            if label not in self.labels:
                self._append_placeholder_label(label)
            else:
                self._append_value(self.labels[label], width=2)

        elif token == "-":  # a negative literal split into two tokens
            value_token = self._next_token()
            if not re.match(VALUE_RE, value_token):
                print(f"Syntax error: -{value_token}")
                exit(1)
            width = self._next_immediate_width()
            mask = 0xFF if width == 1 else 0xFFFF
            self._append_value((-int(value_token, 0)) & mask, width=width)

        elif token.startswith("'"):  # a char literal
            self._process_token(str(_char_literal_value(token)))

        elif re.match(VALUE_RE, token):  # raw immediate, width depends on the operand/instruction
            width = self._next_immediate_width()
            mask = 0xFF if width == 1 else 0xFFFF
            self._append_value(int(token, 0) & mask, width=width)

        elif re.match(WHITESPACE_RE, token):
            pass

        else:
            print(f"Syntax error: {token}")
            exit(1)

    def _next_immediate_width(self):
        # Byte width of the next immediate operand for the most recently emitted instruction,
        # defaults to 2 once that instruction's narrow operands (if any) are consumed
        return self.pending_widths.pop(0) if self.pending_widths else 2

    def _append_value(self, value, width=None):
        # Appends a value, narrow (1 byte) or full (2 bytes) little-endian
        pos = self.position - self.offset

        if width is None:
            width = 2 if value > 0xFF else 1

        if width == 2:
            assert self.output[pos] is None and self.output[pos + 1] is None
            self.output[pos] = value & 0xFF
            self.output[pos + 1] = (value >> 8) & 0xFF
            self.position += 2
        else:
            assert self.output[pos] is None
            self.output[pos] = value & 0xFF
            self.position += 1

    def _append_placeholder_label(self, label):
        # Reserves space for a label not yet defined, to be filled in on the second pass
        pos = self.position - self.offset
        assert self.output[pos] is None and self.output[pos + 1] is None

        self.todo_labels[self.position] = label
        self.output[pos] = 0x00
        self.output[pos + 1] = 0x00
        self.position += 2

    def _next_token(self):
        self.token_pos += 1
        return self.tokens[self.token_pos]

    def _directive_offset(self):
        # Start address of the file, where the binary is placed on the bus
        self.offset = self.position = int(self._next_token(), 0) & 0xFFFF

    def _directive_seek(self):
        self.position = int(self._next_token(), 0) & 0xFFFF

    def _directive_seekpush(self):
        value = int(self._next_token(), 0) & 0xFFFF
        self.seekstack.append(self.position)
        self.position = value

    def _directive_seekpop(self):
        self.position = self.seekstack.pop(-1)

    def _directive_set(self):
        name = self._next_token()
        value = int(self._next_token(), 0) & 0xFFFF
        self.labels[name] = value

    def _directive_byte(self):
        # Emits raw byte(s) of data, not an instruction, used for ROM data blocks. Accepts a
        # quoted string (one byte per char, no implicit NUL), a char literal, and/or any number
        # of space-separated values on one line
        while True:
            token = self._next_token()
            if token.startswith('"'):
                for c in _unescape(token[1:-1]):
                    self._append_value(ord(c) & 0xFF, width=1)
            elif token.startswith("'"):
                self._append_value(_char_literal_value(token) & 0xFF, width=1)
            else:
                self._append_value(int(token, 0) & 0xFF, width=1)
            if not self._peek_more_directive_args():
                break

    def _directive_word(self):
        # Emits raw 16-bit little-endian value(s), see _directive_byte
        while True:
            token = self._next_token()
            if token.startswith("'"):
                self._append_value(_char_literal_value(token) & 0xFFFF, width=2)
            else:
                self._append_value(int(token, 0) & 0xFFFF, width=2)
            if not self._peek_more_directive_args():
                break

    def _peek_more_directive_args(self):
        # True if the next token is itself a value/string/char, meaning the current directive
        # continues, rather than a label/instruction/directive
        nxt = self.token_pos + 1
        if nxt >= len(self.tokens):
            return False
        token = self.tokens[nxt]
        return bool(re.match(VALUE_RE, token) or token.startswith('"') or token.startswith("'"))


def assemble(source_text):
    return Assembler().assemble(source_text)
