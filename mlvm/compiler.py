import re
import os
import sys
from mlvm.const import *

EXPRESSION_UNARY_OPERATORS = (
    "~"
)

EXPRESSION_OPERATOR_PRECEDENCE = (
    "&&", "==", ">=", "<=", ">", "<", "|", "^", "&", "<<", ">>", "+", "-", "*", "%", "~"
)

EXPRESSION_OPERATOR_INSTRUCTION_MAP = {
    "==": "CMP", ">=": "GTE", "<=": "LTE", ">": "GTC", "<": "LTC", "|": "IOR", "^": "XOR",
    "&": "AND", "<<": "LSS", ">>": "RSS", "+": "ADD", "-": "SUB", "*": "MUL", "~": "NOT",
    "&&": "ANL", "%": "MOD"
}

OPERATORS = (
    "/*", "*/", "==", ">=", "<=", "=", ">>", "<<", ">", "<", "{", "}", "\"", "'", "+", "-", "*",
    "(", ")", "&&", "&", "|", "^", "~", "#", "@", "!", "?", ";", "%"
)

KEYWORDS = [
    "fn", "define", "include", "var", "set", "if", "else",
    "while", "halt", "asm", "begin", "return", "call"
]

if len(sys.argv) < 3:
    print("You must specify an input and output file!")
    exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    with open(input_file, "r") as input_stream:
        mlvc_script = input_stream.read()
except:
    print(f"Failed to open {input_file}!")
    exit(1)


def file_to_tokens(file):
    lexer_regex_s = "( |\\n"

    for operator in OPERATORS:
        operator = '\\' + ('\\'.join(list(operator)))
        lexer_regex_s += f"|{operator}"

    lexer_regex_s += ")"
    tokens = re.split(lexer_regex_s, file)
    tokens = [token for token in tokens if token != ""]

    return tokens

VALUE_RE = "(0x[0-9A-Fa-f]+|0b[01]+|-?[0-9]+)"

SYMBOL_RE = "[a-zA-Z\_]+[a-zA-Z0-9\_]*"

WHITESPACE_RE = "[ \n]+"

class CompilerStateMachine():
    STATE_NONE = 0
    STATE_COMMENT = 1
    STATE_DEFINE = 2
    STATE_VAR = 3
    STATE_FUNCTION_NAME = 4
    STATE_ASM = 5
    STATE_BRACE_CONTENT = 6
    STATE_SET_LHS = 7
    STATE_SET_RHS = 8
    STATE_CALL = 9
    STATE_IF = 10
    STATE_LOOP = 11
    STATE_INCLUDE = 12

    ASM_ELEMENT_TYPE_INSTRUCTION = 1
    ASM_ELEMENT_TYPE_POINTER = 2

    SET_TYPE_SYMBOL = 1
    SET_TYPE_ADDR = 2

    def __init__(self, tokens):
        self.tokens = tokens
        self.asm = ""
        self.conditional_stack = []
        self.loop_stack = []
        self.state_stack = [self.STATE_NONE]
        self.defines = {}
        self.static_vars = {}
        self.function_names = {}
        self.brace_level = 0
        self.current_prog_mem_addr = PROG_MEM_START_ADDR
        self.cur_conditional_id = 0
        self.cur_loop_id = 0
        self.cur_line = 1

        self.define_builder_content = []
        self.define_builder_name = None

        self.function_builder_name = None

        self.asm_block_brace_state = False
        self.asm_block_element_type = None

        self.expression_builder = []

    def generate(self):
        self.asm += "/* Generated by MLVC Compiler */\n\n"
        self.asm += f".offset {hex(ROM_START)}\n"
        self.asm += f".offset {hex(ROM_SIZE)}\n\n"
        self.asm += f"LND $mlvc_program_start JMP\n\n"

        for token in self.tokens:
            self.process(token)

        return self.asm

    def syntax_error(self, msg):
        print(f"SYNTAX ERROR ON LINE {self.cur_line}: {msg}")
        exit(1)

    def memory_error(self, msg):
        print(f"MEMORY ERROR: {msg}")
        exit(2)

    def process_keyword(self, token):
        if token == "define":
            self.state_stack.append(self.STATE_DEFINE)
            self.define_builder_content = []
            self.define_builder_name = None
        
        elif token == "include":
            self.state_stack.append(self.STATE_INCLUDE)

        elif token == "var":
            self.state_stack.append(self.STATE_VAR)
        
        elif token == "begin":
            self.asm += "\nmlvc_program_start:\n"
        
        elif token == "fn":
            if self.STATE_FUNCTION_NAME in self.state_stack:
                self.syntax_error("Cannot nest function definitions!")

            self.state_stack.append(self.STATE_FUNCTION_NAME)
        
        elif token == "return":
            self.append_instruction("RET")
        
        elif token == "asm":
            if self.state == self.STATE_ASM:
                self.syntax_error("Cannot nest asm blocks!")

            self.state_stack.append(self.STATE_ASM)
            self.asm_block_brace_state = False
        
        elif token == "set":
            self.state_stack.append(self.STATE_SET_LHS)
            self.set_type = None
            self.set_dest = None
        
        elif token == "call":
            self.state_stack.append(self.STATE_CALL)

        elif token == "if":
            self.state_stack.append(self.STATE_IF)
            self.expression_builder = []
        
        elif token == "while":
            self.state_stack.append(self.STATE_LOOP)
            self.expression_builder = []

    def process(self, token):
        self.state = self.state_stack[-1]

        if token == "\n":
            self.cur_line += 1

        if self.state == self.STATE_COMMENT:
            if token == "*/":
                self.state_stack.pop(-1)

        elif token == "/*":
            self.state_stack.append(self.STATE_COMMENT)

        elif token in self.defines:
            for dtoken in self.defines[token]:
                self.process(dtoken)

        elif self.state == self.STATE_DEFINE:
            if token == ";":
                if self.define_builder_name is None:
                    self.syntax_error("Empty define!")

                self.state_stack.pop(-1)
                self.defines[self.define_builder_name] = self.define_builder_content

            else:
                if self.define_builder_name is None:
                    if re.match(SYMBOL_RE, token):
                        self.define_builder_name = token
                    else:
                        if not re.match(WHITESPACE_RE, token):
                            self.syntax_error("Malformed define name!")

                else:
                    self.define_builder_content.append(token)
        
        elif re.match(WHITESPACE_RE, token):
            pass
            
        elif self.state == self.STATE_INCLUDE:
            if not re.match(SYMBOL_RE, token):
                if token == ";":
                    self.state_stack.pop(-1)
                else:
                    self.syntax_error("Malformed module name!")
            else:
                filename = token
                with open(os.path.join(cwd, f"{filename}.mlvc"), "r") as include_file:
                    self.asm += f"\n/* Begin MLVC include {filename} */\n"
                    include_file_text = include_file.read()
                    include_file_tokens = file_to_tokens(include_file_text)
                    self.state_stack.append(self.STATE_NONE)

                    for token in include_file_tokens:
                        self.process(token)
                    
                    self.asm += f"\n/* End MLVC include {filename} */\n\n"

        elif self.state == self.STATE_VAR:
            if not re.match(SYMBOL_RE, token):
                if token == ";":
                    self.state_stack.pop(-1)
                else:
                    self.syntax_error("Malformed var name!")
            else:
                self.allocate_static_var(token, 1)

        elif self.state == self.STATE_FUNCTION_NAME:
            if self.function_builder_name is None:
                if not re.match(SYMBOL_RE, token):
                    self.syntax_error("Malformed function name!")
                else:
                    self.allocate_function(token)
                    self.function_builder_name = token
            else:
                if token != "{":
                    self.syntax_error("Did not open function content!")
                else:
                    self.state_stack.append(self.STATE_BRACE_CONTENT)
        
        elif self.state == self.STATE_ASM:
            if self.asm_block_brace_state:
                if token == "{":
                    self.syntax_error("Cannot use braces inside asm block!")
                elif token == "}":
                    self.asm += "    /* End MLVC asm block */\n"
                    self.asm_block_brace_state = False
                    self.state_stack.pop(-1)
                else:
                    if self.asm_block_element_type is not None:
                        if self.asm_block_element_type == self.ASM_ELEMENT_TYPE_INSTRUCTION:
                            self.append_instruction(token)
                        elif self.asm_block_element_type == self.ASM_ELEMENT_TYPE_POINTER:
                            if token in self.static_vars:
                                self.append_instruction(f"${self.asm_prefix_var(token)}")
                            else:
                                self.syntax_error(f"Variable not defined: {token}!")

                        self.asm_block_element_type = None

                    else:
                        if token == "#":
                            self.asm_block_element_type = self.ASM_ELEMENT_TYPE_INSTRUCTION
                        elif token == "@":
                            self.asm_block_element_type = self.ASM_ELEMENT_TYPE_POINTER
                        elif re.match(VALUE_RE, token):
                            self.append_instruction(token)

            elif token == "{":
                self.asm += "    /* Begin MLVC asm block */\n"
                self.asm_block_brace_state = True


        elif self.state == self.STATE_SET_LHS:
            if re.match(SYMBOL_RE, token):
                self.set_type = self.SET_TYPE_SYMBOL
                if token in self.static_vars:
                    self.set_dest = token
                else:
                    self.syntax_error(f"Undefined symbol: {token}!")

            elif re.match(VALUE_RE, token):
                self.set_type = self.SET_TYPE_ADDR
                self.set_dest = token
            
            elif token == "=":
                if self.set_type is None:
                    self.syntax_error("No left hand side in set!")

                self.state_stack.pop(-1)
                self.state_stack.append(self.STATE_SET_RHS)
                self.expression_builder = []
            
            else:
                self.syntax_error("Malformed left hand side of set!")
        
        elif self.state == self.STATE_SET_RHS:
            if token == ';':
                output_register = self.solve_expression(self.expression_builder)

                if self.set_type == self.SET_TYPE_ADDR:
                    self.append_instruction(f"LND {self.set_dest} WR{output_register}")
                elif self.set_type == self.SET_TYPE_SYMBOL:
                    self.append_instruction(f"LND ${self.asm_prefix_var(self.set_dest)} WR{output_register}")
                else:
                    self.syntax_error("Unknown problem in set!")

                self.state_stack.pop(-1)
            else:
                self.expression_builder.append(token)

        elif self.state == self.STATE_CALL:
            if token == ";":
                self.state_stack.pop(-1)
            elif re.match(SYMBOL_RE, token):
                self.function_call(token)
            else:
                self.syntax_error(f"Invalid function name: {token}!")

        elif self.state == self.STATE_IF:
            if token == "{":
                self.asm += "    /* MLVC if expression */\n"
                output_register = self.solve_expression(self.expression_builder)
                self.conditional_stack.append(self.cur_conditional_id)
                self.asm += f"    LND $conditional_{self.cur_conditional_id}_else JN{output_register} /* MLVC if conditional */\n"
                self.cur_conditional_id += 1
                self.state_stack.append(self.STATE_BRACE_CONTENT)
            else:
                self.expression_builder.append(token)

        elif self.state == self.STATE_LOOP:
            if token == "{":
                self.loop_stack.append(self.cur_loop_id)
                self.asm += f"loop_{self.cur_loop_id}_begin: /* Begin MLVC while block */\n"
                self.asm += "    /* MLVC if expression */\n"
                output_register = self.solve_expression(self.expression_builder)
                self.asm += f"    LND $loop_{self.cur_loop_id}_end JN{output_register} /* MLVC while conditional */\n"
                self.cur_loop_id += 1
                self.state_stack.append(self.STATE_BRACE_CONTENT)
            else:
                self.expression_builder.append(token)

        else:
            if token in KEYWORDS:
                self.process_keyword(token)
            
            elif token in OPERATORS:
                if token == "{":
                    self.state_stack.append(self.STATE_BRACE_CONTENT)
                elif token == "}":
                    self.state_stack.pop(-1)

                    if self.state_stack[-1] == self.STATE_FUNCTION_NAME:
                        self.state_stack.pop(-1)
                        self.function_builder_name = None
                        self.append_instruction("RET")
                        self.asm += "\n"
                    
                    elif self.state_stack[-1] == self.STATE_IF:
                        self.state_stack.pop(-1)
                        conditional_id = self.conditional_stack.pop(-1)
                        self.asm += f"conditional_{conditional_id}_else: /* End MLVC if statement */\n"

                    elif self.state_stack[-1] == self.STATE_LOOP:
                        self.state_stack.pop(-1)
                        loop_id = self.loop_stack.pop(-1)
                        self.append_instruction(f"LND $loop_{loop_id}_begin JMP")
                        self.asm += f"loop_{loop_id}_end: /* End MLVC while block */\n"

            elif re.match(VALUE_RE, token):
                pass
            
            elif re.match(SYMBOL_RE, token):
                pass
            
            else:
                self.syntax_error(f"Illegal token: {token}")

    def asm_prefix_var(self, varname):
        return f"mlvc_static_var_{varname}"
    
    def asm_prefix_function(self, fname):
        return f"mlvc_function_{fname}"

    def allocate_static_var(self, varname, size):
        if self.current_prog_mem_addr == PROG_MEM_END_ADDR:
            self.memory_error("Out of program memory!")

        if varname in KEYWORDS:
            self.syntax_error(f"{varname} is a reserved keyword!")

        if varname in self.static_vars or varname in self.function_names:
            self.syntax_error(f"Symbol {varname} previously defined!")

        self.static_vars[varname] = self.current_prog_mem_addr
        self.current_prog_mem_addr += size

        self.asm += f".set {self.asm_prefix_var(varname)} {hex(self.static_vars[varname])}\n"

    def allocate_function(self, fname):
        if fname in KEYWORDS:
            self.syntax_error(f"{fname} is a reserved keyword!")
        
        if fname in self.static_vars or fname in self.function_names:
            self.syntax_error(f"Symbol {fname} previously defined!")
        
        self.function_names[fname] = self.asm_prefix_function(fname)

        self.asm += f"\n/* MLVC function {fname} */\n"
        self.asm += f"{self.function_names[fname]}:\n"
    
    def append_instruction(self, instruction):
        self.asm += f"    {instruction}\n"

    def infix_to_rpn(self, expression):
        output = []
        stack = []

        for token in expression:
            if token in EXPRESSION_OPERATOR_PRECEDENCE:
                while len(stack) and stack[-1] != "(" and stack[-1] in EXPRESSION_OPERATOR_PRECEDENCE and EXPRESSION_OPERATOR_PRECEDENCE.index(token) <= EXPRESSION_OPERATOR_PRECEDENCE.index(stack[-1]):
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
                output.append(token)

        while len(stack):
            if stack[-1] == "(" or stack[-1] == ")":
                self.syntax_error("Mismatched parentheses!")

            output.append(stack.pop())

        return output

    def solve_expression(self, expression):
        if len(expression) == 0:
            self.syntax_error("Cannot solve empty expression!")

        rpn = self.infix_to_rpn(expression.copy())
        output_register = None

        stack = []

        def get_element(e, reg):
            if e is None:
                self.append_instruction(f"PUL S{reg}C")
            elif re.match(VALUE_RE, e):
                self.append_instruction(f"LN{reg} {e}")
            elif re.match(SYMBOL_RE, e):
                if not e in self.static_vars:
                    self.syntax_error(f"Undefined symbol: {e}!")

                self.append_instruction(f"LND ${self.asm_prefix_var(e)} RD{reg}")
            else:
                self.syntax_error("Bad expression!")

        for i, element in enumerate(rpn):
            if element in EXPRESSION_OPERATOR_PRECEDENCE:
                get_element(stack.pop(), "B")
                get_element(stack.pop(), "A")
                self.append_instruction(EXPRESSION_OPERATOR_INSTRUCTION_MAP[element])
                if i == (len(rpn) - 1):
                    output_register = "C"
                else:
                    self.append_instruction("PSH")
                    stack.append(None) # Pushed onto real stack, pull off later
            else:
                stack.append(element)

        if len(stack):
            get_element(stack.pop(), "A")
            output_register = "A"

        return output_register

    def function_call(self, fname):
        self.asm += f"    LND ${self.asm_prefix_function(fname)} SRT /* Calling MLVC function {fname} */\n"

cwd = os.path.join(*os.path.split(input_file)[:-1])

csm = CompilerStateMachine(file_to_tokens(mlvc_script))

asm = csm.generate()

print(asm)

try:
    with open(output_file, "w") as output_stream:
        output_stream.write(asm)
except:
    print(f"Failed to open {output_file}!")
    exit(1)
