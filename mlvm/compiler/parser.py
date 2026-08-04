"""
Turns a token stream into a list of AST statements, populating a SymbolTable as it goes.
"""

import os
import re

from .lexer import Token, tokenize
from .errors import CompileError, MlvcSyntaxError
from .symbols import LocalScope
from .ast_nodes import (
    Expr,
    StaticVarDecl,
    StaticBlockDecl,
    DataBlockDecl,
    FunctionDecl,
    BeginMarker,
    MacroExpansionComment,
    SymbolTarget,
    DerefTarget,
    FieldTarget,
    SetStmt,
    CallStmt,
    IncrDecrStmt,
    ReturnStmt,
    RtiStmt,
    FrameOpStmt,
    IfStmt,
    WhileStmt,
    AsmBlock,
    AsmToken,
    AsmAddressOf,
    AsmLabel,
    AsmDirective,
)
from .grammar import (
    KEYWORDS,
    OPERATORS,
    TYPE_KEYWORDS,
    SYMBOL_RE,
    VALUE_RE,
    FIELD_TOKEN_RE,
    DOT_FIELD_RE,
    EXPRESSION_OPERATOR_PRECEDENCE,
    is_pointer_type,
    is_block_type,
    pointee_type,
    block_element_type,
    unescape_literal,
)

# Keywords with no runtime effect
_DECL_ONLY_KEYWORDS = ("var", "alloc", "data", "struct", "define", "macro")


class Parser:
    def __init__(self, symbols, cwd):
        self.symbols = symbols
        self.cwd = cwd

        self.tokens = []
        self.pos = 0
        self.cur_file = None

        self.local_scope = None  # LocalScope while inside a function, else None
        self.at_function_top_level = False  # directly in a function body, not if/while-nested
        self.local_decls_open = True  # can var/alloc still appear here?

        # A bare string literal operand becomes a hidden, uniquely-named data block
        self.string_literal_counter = 0
        self.pending_data_blocks = []

        # Paths of every included file. Reincluding the same file does nothing
        self.included_files = set()

        # Outermost macro name currently expanding at the cursor, consumed by the next
        # parse_statement() call to annotate the generated .mlvs
        self.pending_macro_name = None

    def parse_program(self, mlvc_filename):
        self.cur_file = mlvc_filename
        with open(mlvc_filename, "r") as f:
            self.tokens = tokenize(f.read())
        self.pos = 0

        try:
            statements = []
            while self.pos < len(self.tokens):
                statements.extend(self.parse_statement())
            statements.extend(self.pending_data_blocks)
            return statements
        except CompileError as e:
            if e.file is None:
                e.file = self.cur_file
                e.line = self._current_line()
            raise

    def _expand_macros_at_cursor(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos] == "#":
            name_idx = self.pos + 1
            if name_idx >= len(self.tokens):
                self.syntax_error("Malformed macro use: expected a name after #!")
            name = self.tokens[name_idx]
            line = self.tokens[self.pos].line

            if name in self.symbols.defines:
                expansion = [Token(str(t), line) for t in self.symbols.defines[name]]
                self.tokens[self.pos : name_idx + 1] = expansion
            elif name in self.symbols.macros:
                self._expand_parametrized_macro_at_cursor(name, name_idx, line)
            else:
                self.syntax_error(f"Undefined macro: {name}!")

    def _split_macro_call_args(self, open_paren_idx):
        """Splits macro arguments by only top-level commas"""
        args = []
        current = []
        depth = 1
        i = open_paren_idx + 1
        while True:
            if i >= len(self.tokens):
                self.syntax_error("Unterminated macro call!")
            token = self.tokens[i]
            if token == "(":
                depth += 1
                current.append(token)
            elif token == ")":
                depth -= 1
                if depth == 0:
                    if current or args:
                        args.append(current)
                    return args, i
                current.append(token)
            elif token == "," and depth == 1:
                args.append(current)
                current = []
            else:
                current.append(token)
            i += 1

    def _expand_parametrized_macro_at_cursor(self, name, name_idx, line):
        params, body = self.symbols.macros[name]

        open_paren_idx = name_idx + 1
        if open_paren_idx >= len(self.tokens) or self.tokens[open_paren_idx] != "(":
            self.syntax_error(f"Macro {name} used without arguments - expected (!")

        args, close_idx = self._split_macro_call_args(open_paren_idx)
        if len(args) != len(params):
            self.syntax_error(f"Macro {name} expects {len(params)} argument(s), got {len(args)}!")
        arg_map = dict(zip(params, args))

        if self.pending_macro_name is None:
            self.pending_macro_name = name

        # Substitutes each #PARAM with its argument's tokens
        expansion = []
        i = 0
        while i < len(body):
            token = body[i]
            if token == "#" and i + 1 < len(body) and str(body[i + 1]) in arg_map:
                expansion.extend(Token(str(t), line) for t in arg_map[str(body[i + 1])])
                i += 2
            else:
                expansion.append(Token(str(token), line))
                i += 1

        self.tokens[self.pos : close_idx + 1] = expansion

    def peek(self):
        self._expand_macros_at_cursor()
        if self.pos >= len(self.tokens):
            self.syntax_error("Unexpected end of file!")
        return self.tokens[self.pos]

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def advance_raw(self):
        if self.pos >= len(self.tokens):
            self.syntax_error("Unexpected end of file!")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expect(self, value):
        token = self.advance()
        if token != value:
            self.syntax_error(f"Expected {value!r}, got {token!r}!")
        return token

    def _current_line(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos].line
        return self.tokens[-1].line if self.tokens else 0

    def syntax_error(self, msg):
        raise MlvcSyntaxError(msg)

    def parse_symbol_name(self, what, raw=False):
        token = self.advance_raw() if raw else self.advance()
        if not re.match(SYMBOL_RE, token):
            self.syntax_error(f"Malformed {what} name!")
        return str(token)

    def parse_optional_address(self, what):
        # var/alloc/fn @ 0xADDR pins to a fixed address
        if self.peek() != "@":
            return None
        self.advance()
        addr_token = self.advance()
        if not re.match(VALUE_RE, addr_token):
            self.syntax_error(f"Malformed {what} address!")
        return int(addr_token, 0)

    def parse_statement(self):
        """Returns a list of 0+ AST nodes (0 for pure symbol-table declarations, more than 1 for
        include and bare { } blocks, 1 otherwise)."""
        token = self.peek()  # may trigger #NAME(...) macro expansion, see pending_macro_name

        name = self.pending_macro_name
        self.pending_macro_name = None

        statements = self._parse_statement_body(token)

        if name is not None:
            return [MacroExpansionComment(name)] + statements
        return statements

    def _parse_statement_body(self, token):
        if token in KEYWORDS:
            if token not in _DECL_ONLY_KEYWORDS and self.local_scope is not None:
                self.local_decls_open = False
            return self._parse_keyword_statement(token)

        if token in OPERATORS:
            if token == "{":  # a bare anonymous block, just groups statements
                return self.parse_nested_block()
            if token == "}":
                self.syntax_error("Unexpected }!")
            # any other stray operator does nothing
            self.advance()
            return []

        if re.match(VALUE_RE, token):
            self.syntax_error(f"Unexpected literal: {token}")
        if re.match(SYMBOL_RE, token):
            self.syntax_error(f"Unexpected symbol: {token}")
        self.syntax_error(f"Illegal token: {token}")

    def _parse_keyword_statement(self, token):
        if token == "define":
            self.advance()
            self.parse_define()
            return []
        if token == "macro":
            self.advance()
            self.parse_macro()
            return []
        if token == "include":
            self.advance()
            return self.parse_include()
        if token == "var":
            return self.parse_var_decl()
        if token == "alloc":
            node = self.parse_alloc_decl()
            return [node] if node is not None else []
        if token == "data":
            return [self.parse_data_decl()]
        if token == "struct":
            self.parse_struct_decl()
            return []
        if token == "fn":
            return [self.parse_function_decl()]
        if token == "begin":
            self.advance()
            return [BeginMarker()]
        if token == "return":
            return [self.parse_return_stmt()]
        if token == "rti":
            return [self.parse_rti_stmt()]
        if token in ("svi", "ldi"):
            return [self.parse_frame_op_stmt()]
        if token == "asm":
            return [self.parse_asm_block()]
        if token == "set":
            return [self.parse_set_stmt()]
        if token == "call":
            return [self.parse_call_stmt()]
        if token in ("incr", "decr"):
            return [self.parse_incr_decr_stmt()]
        if token == "if":
            return [self.parse_if_stmt()]
        if token == "while":
            return [self.parse_while_stmt()]

        self.syntax_error(f"Unexpected keyword: {token}")

    def parse_block(self):
        self.expect("{")
        statements = []
        while self.peek() != "}":
            statements.extend(self.parse_statement())
        self.advance()  # '}'
        return statements

    def parse_nested_block(self):
        # var/alloc may only appear directly in a function body, not in a nested if/while block
        prev_top_level = self.at_function_top_level
        self.at_function_top_level = False
        try:
            return self.parse_block()
        finally:
            self.at_function_top_level = prev_top_level

    def parse_type_prefix(self):
        token = self.advance()
        if token == "[":
            inner = self.advance()
            if inner not in TYPE_KEYWORDS and inner not in self.symbols.structs:
                self.syntax_error("Pointer type must wrap a type or struct name, e.g. [u16] or [proc_t]!")
            self.expect("]")
            return str(inner) + "*"
        if token in TYPE_KEYWORDS or token in self.symbols.structs:
            return str(token)
        self.syntax_error("Expected a type (u8, u16, i8, i16, a struct name, or [type] for a pointer)!")

    def _check_local_decl_position(self, keyword):
        if self.local_scope is None:
            return
        if not self.at_function_top_level:
            self.syntax_error(f"{keyword} declarations inside a function must not be nested in if/while blocks!")
        if not self.local_decls_open:
            self.syntax_error(f"{keyword} declarations inside a function must come before any other statement!")

    def _declare_scalar(self, name, var_type, address):
        if self.local_scope is not None:
            if address is not None:
                self.syntax_error(f"Cannot pin local variable {name} to a fixed address!")
            self.local_scope.declare_var(name, var_type, self.symbols)
            return None
        addr = self.symbols.declare_static_var(name, var_type, address=address)
        return StaticVarDecl(name, addr)

    def _declare_block(self, name, elem_type, count, address):
        if self.local_scope is not None:
            if address is not None:
                self.syntax_error(f"Cannot pin local block {name} to a fixed address!")
            self.local_scope.declare_block(name, elem_type, count, self.symbols)
            return None
        addr = self.symbols.declare_static_block(name, elem_type, count, address=address)
        return StaticBlockDecl(name, addr)

    def parse_var_decl(self):
        self._check_local_decl_position("var")
        self.advance()  # 'var'
        var_type = self.parse_type_prefix()

        nodes = []
        while True:
            name = self.parse_symbol_name("var")
            address = self.parse_optional_address("var")

            node = self._declare_scalar(name, var_type, address)
            if node is not None:
                nodes.append(node)

            if self.peek() == ";":
                self.advance()
                return nodes

    def parse_alloc_decl(self):
        self._check_local_decl_position("alloc")
        self.advance()  # 'alloc'
        elem_type = self.parse_type_prefix()

        count_token = self.advance()
        if not re.match(VALUE_RE, count_token):
            self.syntax_error("alloc must specify an element count!")
        count = int(count_token, 0)

        name = self.parse_symbol_name("alloc")
        address = self.parse_optional_address("alloc")

        self.expect(";")
        return self._declare_block(name, elem_type, count, address)

    def parse_data_decl(self):
        # data TYPE NAME { v1, v2, ... }; / data TYPE NAME "text";
        self.advance()  # 'data'
        elem_type = self.parse_type_prefix()
        if elem_type not in TYPE_KEYWORDS:
            self.syntax_error(f"data blocks must be a scalar type (u8/u16/i8/i16), not {elem_type}!")

        name = self.parse_symbol_name("data block")

        source_string = self.peek() if self.peek().startswith('"') else None
        values = self._parse_data_initializer()
        self.expect(";")

        mask = 0xFF if self.symbols.type_size(elem_type) == 1 else 0xFFFF
        values = [v & mask for v in values]

        self.symbols.declare_data_block(name, elem_type)
        return DataBlockDecl(name=name, elem_type=elem_type, values=values, source_string=source_string)

    def _parse_data_initializer(self):
        if self.peek().startswith('"'):
            return self._string_literal_bytes(self.advance())

        self.expect("{")
        values = []
        if self.peek() != "}":
            while True:
                values.append(self._parse_data_value())
                if self.peek() == ",":
                    self.advance()
                    continue
                break
        self.expect("}")
        return values

    def _parse_data_value(self):
        token = self.advance()
        if token == "-" and re.match(VALUE_RE, self.peek()):
            return int("-" + str(self.advance()), 0)
        if token.startswith("'"):
            return self._char_literal_value(token)
        if re.match(VALUE_RE, token):
            return int(token, 0)
        self.syntax_error(f"Malformed data block value: {token}!")

    def _char_literal_value(self, token):
        inner = unescape_literal(token[1:-1])
        if len(inner) != 1:
            self.syntax_error(f"Malformed char literal: {token}!")
        if ord(inner) > 255:
            self.syntax_error(f"Char literal out of byte range: {token}!")
        return ord(inner)

    def _string_literal_bytes(self, token):
        inner = unescape_literal(token[1:-1])
        values = []
        for c in inner:
            if ord(c) > 255:
                self.syntax_error(f"String literal contains a non-byte character: {token}!")
            values.append(ord(c))
        values.append(0)  # null terminated
        return values

    def _synthesize_string_data_block(self, token):
        # A bare string literal operand becomes a hidden data block, replaced with @name
        values = self._string_literal_bytes(token)
        name = f"mlvc_string_literal_{self.string_literal_counter}"
        self.string_literal_counter += 1
        self.symbols.declare_data_block(name, "u8")
        block = DataBlockDecl(name=name, elem_type="u8", values=values, source_string=str(token))
        self.pending_data_blocks.append(block)
        return name

    def parse_struct_decl(self):
        self.advance()  # 'struct'
        name = self.parse_symbol_name("struct")

        self.expect("{")
        fields = []
        while self.peek() != "}":
            field_type = self.parse_type_prefix()
            if field_type not in TYPE_KEYWORDS and not is_pointer_type(field_type):
                self.syntax_error(f"Struct fields cannot embed another struct by value: {field_type}!")
            field_name = self.parse_symbol_name("struct field")
            self.expect(";")
            fields.append((field_name, field_type))
        self.advance()  # '}'
        self.expect(";")

        self.symbols.declare_struct(name, fields)

    def parse_function_decl(self):
        self.advance()  # 'fn'
        if self.local_scope is not None:
            self.syntax_error("Cannot nest function definitions!")

        name = self.parse_symbol_name("function")
        address = self.parse_optional_address("function")

        params = []
        if self.peek() == "(":
            self.advance()
            params = self.parse_function_params()

        self.expect("{")

        self.symbols.declare_function(name, params, address=address)

        local_scope = LocalScope()
        arg_bytes = sum(self.symbols.type_size(ptype) for _, ptype in params)
        running_offset = 0
        for pname, ptype in params:
            # params have negative offset, sit below the return address SRT pushes
            local_scope.declare_param(pname, ptype, running_offset - arg_bytes - 2)
            running_offset += self.symbols.type_size(ptype)

        prev_scope, prev_top_level, prev_decls_open = (
            self.local_scope,
            self.at_function_top_level,
            self.local_decls_open,
        )
        self.local_scope = local_scope
        self.at_function_top_level = True
        self.local_decls_open = True
        try:
            body = []
            while self.peek() != "}":
                body.extend(self.parse_statement())
            self.advance()  # '}'
        finally:
            self.local_scope, self.at_function_top_level, self.local_decls_open = (
                prev_scope,
                prev_top_level,
                prev_decls_open,
            )

        return FunctionDecl(name=name, address=address, local_scope=local_scope, body=body)

    def parse_function_params(self):
        if self.peek() == ")":
            self.advance()
            return []

        params = []
        while True:
            var_type = self.parse_type_prefix()
            if var_type not in TYPE_KEYWORDS and not is_pointer_type(var_type):
                self.syntax_error(f"Function parameters must be a scalar or pointer type, not {var_type}!")

            name = self.parse_symbol_name("parameter")
            if any(pname == name for pname, _ in params):
                self.syntax_error(f"Duplicate parameter name: {name}!")
            if name in KEYWORDS:
                self.syntax_error(f"{name} is a reserved keyword!")
            if name in self.symbols.static_vars or name in self.symbols.functions:
                self.syntax_error(f"Symbol {name} previously defined!")

            params.append((name, var_type))

            token = self.advance()
            if token == ")":
                return params
            if token != ",":
                self.syntax_error("Expected , or ) in parameter list!")

    def parse_return_stmt(self):
        is_top_level = self.at_function_top_level
        self.advance()  # 'return'
        if self.peek() == ";":
            self.advance()
            return ReturnStmt(value=None, is_top_level=is_top_level)
        value = self.parse_expr_until(";")
        self.advance()  # ';'
        return ReturnStmt(value=value, is_top_level=is_top_level)

    def parse_rti_stmt(self):
        is_top_level = self.at_function_top_level
        self.advance()  # 'rti', no semicolon
        return RtiStmt(is_top_level=is_top_level)

    def parse_frame_op_stmt(self):
        # svi <expr>; / ldi <expr>; evaluates <expr> into C, then emits the bare opcode.
        op = str(self.advance()).upper()  # 'svi'/'ldi' -> 'SVI'/'LDI'
        value = self.parse_expr_until(";")
        self.advance()  # ';'
        return FrameOpStmt(op=op, value=value)

    def parse_set_stmt(self):
        self.advance()  # 'set'
        target = self.parse_set_target()
        self.expect("=")
        value = self.parse_expr_until(";")
        self.advance()  # ';'
        return SetStmt(target=target, value=value)

    def parse_set_target(self):
        token = self.peek()

        if token == "[":  # set [addr] = ...; / set [TYPE expr] = ...; / set [ptr].field = ...;
            self.advance()

            explicit_type = None
            if self.peek() in TYPE_KEYWORDS:
                explicit_type = str(self.advance())

            # Scan for the matching ]. A single token (literal or named pointer/block var) takes
            # the basic path below, while multi-token needs the general computed-address path.
            inner = []
            depth = 1
            while True:
                tok = self.advance()
                if tok == "[":
                    depth += 1
                elif tok == "]":
                    depth -= 1
                    if depth == 0:
                        break
                inner.append(tok)
            if len(inner) == 0:
                self.syntax_error("Malformed pointer dereference!")

            if len(inner) == 1:
                dest_token = inner[0]
                if re.match(VALUE_RE, dest_token):
                    dest = str(dest_token)
                elif re.match(SYMBOL_RE, dest_token):
                    var_type = self.symbols.resolve_type(dest_token, self.local_scope)
                    if var_type is None or not (is_pointer_type(var_type) or is_block_type(var_type)):
                        self.syntax_error(f"{dest_token} is not a pointer or memory block!")
                    if self.symbols.is_read_only(dest_token):
                        self.syntax_error(f"{dest_token} is a data block and is read-only!")
                    dest = str(dest_token)
                else:
                    self.syntax_error("Malformed pointer dereference!")

                if self.peek() == "=":
                    return DerefTarget(dest=dest, explicit_type=explicit_type)

                if explicit_type is not None:
                    self.syntax_error("Cannot combine an explicit type with .field access!")

                field_token = self.advance()
                field_match = re.fullmatch(DOT_FIELD_RE, field_token)
                if not field_match:
                    self.syntax_error("Malformed left hand side of set!")
                field_name = field_match.group(1)
                self.check_deref_field(dest, field_name)
                return FieldTarget(kind="deref", base=dest, field=field_name)

            # A multi-token computed address, explicit_type is mandatory
            if explicit_type is None:
                self.syntax_error(
                    "A computed pointer dereference needs an explicit type, e.g. set [u16 expr] = value;!"
                )
            return DerefTarget(expr=self.make_expr(inner), explicit_type=explicit_type)

        if re.fullmatch(FIELD_TOKEN_RE, token):  # name.field = ...; a direct struct variable
            self.advance()
            field_match = re.fullmatch(FIELD_TOKEN_RE, token)
            base_name, field_name = field_match.group(1), field_match.group(2)
            self.check_direct_field(base_name, field_name)
            return FieldTarget(kind="direct", base=base_name, field=field_name)

        if re.match(SYMBOL_RE, token):
            self.advance()
            name = str(token)

            if self.peek() == "<":  # name<index>.field = ...; an array of structs
                self.advance()
                index_tokens = []
                while self.peek() != ">":
                    index_tokens.append(self.advance())
                self.advance()  # '>'
                field_token = self.advance()
                field_match = re.fullmatch(DOT_FIELD_RE, field_token)
                if not field_match:
                    self.syntax_error("Expected .field after array index in set!")
                field_name = field_match.group(1)
                self.check_index_field(name, field_name)
                return FieldTarget(kind="index", base=name, field=field_name, index_expr=self.make_expr(index_tokens))

            var_type = self.symbols.resolve_type(name, self.local_scope)
            if var_type is None:
                self.syntax_error(f"Undefined symbol: {name}!")
            if is_block_type(var_type):
                self.syntax_error(f"{name} is a memory block; use [{name}] to write to it!")
            return SymbolTarget(name=name)

        self.syntax_error("Malformed left hand side of set!")

    def parse_call_stmt(self):
        self.advance()  # 'call'
        name_token = self.advance()
        if not re.match(SYMBOL_RE, name_token):
            self.syntax_error(f"Invalid function name: {name_token}!")
        fn_name = str(name_token)

        tokens = []
        while self.peek() != ";":
            tokens.append(self.advance())
        self.advance()  # ';'

        args = [self.make_expr(arg_tokens) for arg_tokens in self.split_call_args(tokens)]
        self.check_call(fn_name, args)
        return CallStmt(fn_name=fn_name, args=args)

    def check_call(self, fn_name, args):
        # Validated at parse time so a bad call reports a real file/line
        if fn_name not in self.symbols.functions:
            self.syntax_error(f"Undefined function: {fn_name}!")
        params = self.symbols.functions[fn_name].params
        if len(args) != len(params):
            self.syntax_error(f"{fn_name} expects {len(params)} argument(s), got {len(args)}!")

    def split_call_args(self, tokens):
        if len(tokens) == 0:
            return []

        if tokens[0] != "(" or tokens[-1] != ")":
            self.syntax_error("call arguments must be wrapped in parentheses: call fn_name(args);")

        inner = tokens[1:-1]
        if len(inner) == 0:
            return []

        args, current, depth = [], [], 0
        for tok in inner:
            if tok == "(":
                depth += 1
                current.append(tok)
            elif tok == ")":
                depth -= 1
                current.append(tok)
            elif tok == "," and depth == 0:
                args.append(current)
                current = []
            else:
                current.append(tok)
        args.append(current)
        return args

    def parse_incr_decr_stmt(self):
        op = str(self.advance())  # 'incr' | 'decr'
        name_token = self.advance()
        if not re.match(SYMBOL_RE, name_token):
            self.syntax_error(f"Invalid {op} target: {name_token}!")
        name = str(name_token)
        var_type = self.symbols.resolve_type(name, self.local_scope)
        if var_type is None:
            self.syntax_error(f"Undefined symbol: {name}!")
        if var_type not in TYPE_KEYWORDS and not is_pointer_type(var_type):
            self.syntax_error(f"{op} requires a scalar or pointer variable, not {name}!")
        self.expect(";")
        return IncrDecrStmt(op=op, target=name)

    def parse_if_stmt(self):
        self.advance()  # 'if'
        condition = self.parse_expr_until("{")
        body = self.parse_nested_block()

        else_body = None
        if self.peek() == "else":
            self.advance()  # 'else'
            # else if chains are done internally via nesting, the else branch is a single-statement body with another if
            else_body = [self.parse_if_stmt()] if self.peek() == "if" else self.parse_nested_block()

        return IfStmt(condition=condition, body=body, else_body=else_body)

    def parse_while_stmt(self):
        self.advance()  # 'while'
        condition = self.parse_expr_until("{")
        return WhileStmt(condition=condition, body=self.parse_nested_block())

    def parse_asm_block(self):
        self.advance()  # 'asm'
        self.expect("{")

        lines = []
        while self.peek() != "}":
            token = self.advance()

            if token == "{":
                self.syntax_error("Cannot use braces inside asm block!")

            elif token == "@":
                name_token = self.advance()
                if name_token not in self.symbols.static_vars and name_token not in self.symbols.functions:
                    self.syntax_error(f"Variable not defined: {name_token}!")
                lines.append(AsmAddressOf(str(name_token)))

            elif token.startswith("."):  # a directive
                parts = [str(token)]
                start_line = token.line
                while self.peek() != "}" and self.peek().line == start_line:
                    parts.append(str(self.advance()))
                lines.append(AsmDirective(" ".join(parts)))

            elif re.fullmatch(SYMBOL_RE + ":", token):
                lines.append(AsmLabel(str(token)))

            else:
                lines.append(AsmToken(str(token)))

        self.advance()  # '}'
        return AsmBlock(lines=lines)

    def parse_define(self):
        name = self.parse_symbol_name("define", raw=True)

        content = []
        while True:
            token = self.advance_raw()
            if token == ";":
                break
            content.append(token)

        self.symbols.defines[name] = content

    def parse_macro(self):
        name = self.parse_symbol_name("macro", raw=True)

        if self.advance_raw() != "(":
            self.syntax_error(f"Expected ( after macro name {name}!")

        params = []
        first = self.advance_raw()
        if first != ")":
            while True:
                if not re.match(SYMBOL_RE, first):
                    self.syntax_error("Malformed macro parameter name!")
                params.append(str(first))
                sep = self.advance_raw()
                if sep == ")":
                    break
                if sep != ",":
                    self.syntax_error("Expected , or ) in macro parameter list!")
                first = self.advance_raw()

        if self.advance_raw() != "{":
            self.syntax_error(f"Expected {{ to begin macro {name}'s body!")

        body = []
        depth = 1
        while True:
            token = self.advance_raw()
            if token == "{":
                depth += 1
            elif token == "}":
                depth -= 1
                if depth == 0:
                    break
            body.append(token)

        self.symbols.macros[name] = (params, body)

    def parse_include(self):
        path_parts = []
        while True:
            token = self.advance()
            if token == ";":
                break
            if token != "/":
                path_parts.append(str(token))

        return self.parse_include_file(os.path.join(*path_parts))

    def parse_include_file(self, filename):
        full_path = os.path.join(self.cwd, filename)

        canonical_path = os.path.normcase(os.path.realpath(full_path))
        if canonical_path in self.included_files:
            return []
        self.included_files.add(canonical_path)

        with open(full_path, "r") as f:
            included_tokens = tokenize(f.read())

        prev_file, prev_tokens, prev_pos = self.cur_file, self.tokens, self.pos
        prev_name = self.pending_macro_name
        self.cur_file, self.tokens, self.pos = full_path, included_tokens, 0
        self.pending_macro_name = None

        statements = []
        while self.pos < len(self.tokens):
            statements.extend(self.parse_statement())

        self.cur_file, self.tokens, self.pos = prev_file, prev_tokens, prev_pos
        self.pending_macro_name = prev_name
        return statements

    # Struct field access validation
    def check_direct_field(self, base_name, field_name):
        base_type = self.symbols.resolve_type(base_name, self.local_scope)
        if base_type is None:
            self.syntax_error(f"Undefined symbol: {base_name}!")
        if is_pointer_type(base_type):
            self.syntax_error(f"{base_name} is a pointer; use [{base_name}].{field_name} instead!")
        if base_type not in self.symbols.structs:
            self.syntax_error(f"{base_name} is not a struct!")
        if field_name not in self.symbols.structs[base_type].fields:
            self.syntax_error(f"{base_type} has no field {field_name}!")

    def check_deref_field(self, ptr_name, field_name):
        base_type = self.symbols.resolve_type(ptr_name, self.local_scope)
        if base_type is None:
            self.syntax_error(f"Undefined symbol: {ptr_name}!")
        if not is_pointer_type(base_type) or pointee_type(base_type) not in self.symbols.structs:
            self.syntax_error(f"{ptr_name} is not a pointer to a struct!")
        struct_name = pointee_type(base_type)
        if field_name not in self.symbols.structs[struct_name].fields:
            self.syntax_error(f"{struct_name} has no field {field_name}!")

    def check_index_field(self, base_name, field_name):
        base_type = self.symbols.resolve_type(base_name, self.local_scope)
        if base_type is None:
            self.syntax_error(f"Undefined symbol: {base_name}!")
        if not is_block_type(base_type) or block_element_type(base_type) not in self.symbols.structs:
            self.syntax_error(f"{base_name} is not an array of structs!")
        struct_name = block_element_type(base_type)
        if field_name not in self.symbols.structs[struct_name].fields:
            self.syntax_error(f"{struct_name} has no field {field_name}!")

    def make_expr(self, tokens):
        return Expr(rpn=self.infix_to_rpn(list(tokens)))

    def parse_expr_until(self, *terminators):
        tokens = []
        while self.peek() not in terminators:
            tokens.append(self.advance())
        return self.make_expr(tokens)

    def infix_to_rpn(self, expression):
        """Converts an infix token list to RPN using operator precedence and parentheses."""
        output = []
        stack = []

        i = 0
        while i < len(expression):
            token = expression[i]

            if token.startswith("'"):  # a char literal
                output.append(str(self._char_literal_value(token)))
                i += 1
                continue

            if token.startswith('"'):  # a string literal
                output.append(f"@{self._synthesize_string_data_block(token)}")
                i += 1
                continue

            if token == "[":  # [ expr ] / [ TYPE expr ] dereference, optionally followed by .field
                depth = 1
                j = i + 1
                while j < len(expression) and depth > 0:
                    if expression[j] == "[":
                        depth += 1
                    elif expression[j] == "]":
                        depth -= 1
                    j += 1

                if depth != 0:
                    self.syntax_error("Malformed pointer dereference!")

                inner = expression[i + 1 : j - 1]
                if len(inner) == 0:
                    self.syntax_error("Malformed pointer dereference!")

                explicit_type = None
                if str(inner[0]) in TYPE_KEYWORDS:
                    explicit_type = str(inner[0])
                    inner = inner[1:]
                    if len(inner) == 0:
                        self.syntax_error("Malformed pointer dereference: missing expression after type!")

                dot_match = j < len(expression) and re.fullmatch(DOT_FIELD_RE, expression[j])
                if dot_match:  # [ptr].field struct pointer field access
                    if explicit_type is not None:
                        self.syntax_error("Cannot combine an explicit type with .field access!")
                    if len(inner) != 1:
                        self.syntax_error("[...].field requires a pointer-to-struct variable, e.g. [ptr].field!")
                    self.check_deref_field(str(inner[0]), dot_match.group(1))
                    output.append(("deref_field", inner, dot_match.group(1)))
                    i = j + 1
                    continue

                # inner kept as raw tokens too, since codegen has special cases for a single bare symbol
                output.append(("deref", inner, self.make_expr(inner), explicit_type))
                i = j
                continue

            if token == "<":
                is_index = (
                    i > 0 and re.match(SYMBOL_RE, expression[i - 1]) and len(output) and output[-1] == expression[i - 1]
                )

                if is_index:
                    depth = 0
                    j = i + 1
                    close = None
                    while j < len(expression):
                        if expression[j] == "(":
                            depth += 1
                        elif expression[j] == ")":
                            depth -= 1
                        elif expression[j] == ">" and depth == 0:
                            close = j
                            break
                        j += 1

                    dot_match = (
                        close is not None
                        and close + 1 < len(expression)
                        and re.fullmatch(DOT_FIELD_RE, expression[close + 1])
                    )

                    if dot_match:
                        index_tokens = expression[i + 1 : close]
                        if len(index_tokens) == 0:
                            self.syntax_error("Malformed array index!")
                        base_name = output.pop()
                        self.check_index_field(str(base_name), dot_match.group(1))
                        output.append(("index_field", base_name, self.make_expr(index_tokens), dot_match.group(1)))
                        i = close + 2
                        continue

            if token == "?":  # ?fn_name(arg1, arg2), a function call usable as an operand
                if i + 1 >= len(expression) or not re.match(SYMBOL_RE, expression[i + 1]):
                    self.syntax_error("Malformed function call: expected a function name after ?!")
                if i + 2 >= len(expression) or expression[i + 2] != "(":
                    self.syntax_error("Malformed function call: expected ( after function name!")
                fn_name = expression[i + 1]

                depth = 1
                j = i + 3
                args_tokens = []
                current = []
                while j < len(expression) and depth > 0:
                    tok = expression[j]
                    if tok == "(":
                        depth += 1
                        current.append(tok)
                    elif tok == ")":
                        depth -= 1
                        if depth == 0:
                            break
                        current.append(tok)
                    elif tok == "," and depth == 1:
                        args_tokens.append(current)
                        current = []
                    else:
                        current.append(tok)
                    j += 1

                if depth != 0:
                    self.syntax_error("Malformed function call: missing )!")
                if current or args_tokens:
                    args_tokens.append(current)

                call_args = [self.make_expr(a) for a in args_tokens]
                self.check_call(str(fn_name), call_args)
                output.append(("call", str(fn_name), call_args))
                i = j + 1
                continue

            if re.fullmatch(FIELD_TOKEN_RE, token):  # name.field, a direct struct var
                field_match = re.fullmatch(FIELD_TOKEN_RE, token)
                self.check_direct_field(field_match.group(1), field_match.group(2))
                output.append(("field", field_match.group(1), field_match.group(2)))
                i += 1
                continue

            if token == "@":  # getting address of symbol, collapse "@ name" into one operand
                if i + 1 >= len(expression):
                    self.syntax_error("Malformed address-of!")
                name = str(expression[i + 1])
                is_local = self.local_scope is not None and name in self.local_scope
                if not is_local and name not in self.symbols.static_vars and name not in self.symbols.functions:
                    self.syntax_error(f"Undefined symbol: {name}!")
                output.append(f"@{name}")
                i += 2
                continue

            if token == "-":
                # Unary only where an operand is expected, start of expression, after another
                # operator, or after "(". Anywhere else "-" is binary subtraction.
                is_unary = i == 0 or expression[i - 1] in EXPRESSION_OPERATOR_PRECEDENCE or expression[i - 1] == "("
                if is_unary and i + 1 < len(expression) and re.fullmatch(VALUE_RE, expression[i + 1]):
                    # directly on a literal: fold the sign into the literal itself, cheaper
                    output.append(f"-{expression[i + 1]}")
                    i += 2
                    continue
                if is_unary:
                    token = "u-"  # special token for unary version of this operator

            if token in EXPRESSION_OPERATOR_PRECEDENCE:
                while (
                    len(stack)
                    and stack[-1] != "("
                    and stack[-1] in EXPRESSION_OPERATOR_PRECEDENCE
                    and EXPRESSION_OPERATOR_PRECEDENCE.index(token) <= EXPRESSION_OPERATOR_PRECEDENCE.index(stack[-1])
                ):
                    output.append(stack.pop())
                stack.append(token)

            elif token == "(":
                stack.append("(")

            elif token == ")":
                while len(stack) and stack[-1] != "(":
                    output.append(stack.pop())
                if stack.pop() != "(":
                    self.syntax_error("Mismatched parentheses!")

            else:
                output.append(str(token))

            i += 1

        while len(stack):
            if stack[-1] == "(" or stack[-1] == ")":
                self.syntax_error("Mismatched parentheses!")
            output.append(stack.pop())

        # A plain symbol reference must be a defined, non-block variable
        for element in output:
            if not isinstance(element, str) or element.startswith("[") or element.startswith("@"):
                continue

            if re.match(VALUE_RE, element) or element in EXPRESSION_OPERATOR_PRECEDENCE:
                continue

            if not re.match(SYMBOL_RE, element):
                self.syntax_error(f"Unknown token in expression: {element}!")

            var_type = self.symbols.resolve_type(element, self.local_scope)
            if var_type is None:
                self.syntax_error(f"Undefined symbol: {element}!")
            if is_block_type(var_type):
                self.syntax_error(
                    f"{element} is a memory block; use @{element} for its address or [{element}] to read it!"
                )

        return output
