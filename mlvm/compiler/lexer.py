"""Turns MLVC source text into a flat list of tokens. Whitespace is dropped, block comments are stripped.

String/char literals get a pre-pass before splitting. The splitter treats operators and spaces as
token boundaries, so "a+b" would otherwise get split into "a, +, b". The pre-pass swaps each quoted
span for a placeholder, then swaps it back once real tokens come out the other side.
"""

import re

from .grammar import OPERATORS

_QUOTED_RE = re.compile(r'"(?:[^"\\\n]|\\.)*"' + r"|'(?:[^'\\\n]|\\.)*'")
_COMMENT_OR_QUOTED_RE = re.compile(r"/\*.*?\*/|" + _QUOTED_RE.pattern, re.DOTALL)


def _build_split_regex():
    parts = ["( |\\n"]
    for operator in OPERATORS:
        parts.append("|\\" + "\\".join(list(operator)))
    parts.append(")")
    return "".join(parts)


_TOKEN_SPLIT_RE = _build_split_regex()


class Token(str):
    """A token's text, plus the source line it came from for error messages."""

    def __new__(cls, value, line):
        obj = str.__new__(cls, value)
        obj.line = line
        return obj


def _extract_quoted_spans(text):
    # Replaces each quoted literal with a placeholder so the splitter can't mess it up. Returns
    # the placeholder text plus a dict mapping each placeholder back to the original span.
    spans = {}

    def replace(m):
        if m.group(0).startswith("/*"):
            return m.group(0)  # a comment, leave as-is
        placeholder = f"\x00STR{len(spans)}\x00"
        spans[placeholder] = m.group(0)
        return placeholder

    return _COMMENT_OR_QUOTED_RE.sub(replace, text), spans


def tokenize(text):
    """Splits text into Tokens. Whitespace/newlines are consumed for line tracking only, never
    emitted. /* ... */ block comments are stripped. A string/char literal always survives as one token."""
    substituted, spans = _extract_quoted_spans(text)

    tokens = []
    line = 1
    in_comment = False

    for raw in re.split(_TOKEN_SPLIT_RE, substituted):
        if raw == "":
            continue

        if raw == "\n":
            line += 1
            continue

        if in_comment:
            if raw == "*/":
                in_comment = False
            continue

        if raw == "/*":
            in_comment = True
            continue

        if raw == " ":
            continue

        tokens.append(Token(spans.get(raw, raw), line))

    return tokens
