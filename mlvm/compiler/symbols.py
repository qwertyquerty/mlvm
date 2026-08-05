"""Symbol tables, built during parsing and used by codegen: static vars, functions,
struct layouts, and macro definitions. LocalScope is for function locals."""

from dataclasses import dataclass, field

from mlvm.const import PROG_MEM_START_ADDR, PROG_MEM_END_ADDR
from .errors import MlvcMemoryError, MlvcSyntaxError
from .grammar import KEYWORDS, var_size


@dataclass
class StructInfo:
    fields: dict  # name -> (offset, type)
    size: int


@dataclass
class FunctionInfo:
    params: list  # (name, type) in declared order
    address: int = None
    defined: bool = False  # False for a forward declaration awaiting its real body


@dataclass
class LocalScope:
    """A function's parameters + var/alloc local"""

    var_offsets: dict = field(default_factory=dict)
    frame_bytes: int = 0  # total bytes of var/alloc locals, excludes parameters

    def check_name_free(self, name, symbols):
        if name in KEYWORDS:
            raise MlvcSyntaxError(f"{name} is a reserved keyword!")
        if name in self.var_offsets or name in symbols.static_vars or name in symbols.functions:
            raise MlvcSyntaxError(f"Symbol {name} previously defined!")

    def declare_param(self, name, var_type, offset):
        self.var_offsets[name] = (offset, var_type)

    def declare_var(self, name, var_type, symbols):
        self.check_name_free(name, symbols)
        self.var_offsets[name] = (self.frame_bytes, var_type)
        self.frame_bytes += symbols.type_size(var_type)

    def declare_block(self, name, elem_type, count, symbols):
        self.check_name_free(name, symbols)
        self.var_offsets[name] = (self.frame_bytes, f"{elem_type}[]")
        self.frame_bytes += symbols.type_size(elem_type) * count

    def __contains__(self, name):
        return name in self.var_offsets


class SymbolTable:
    def __init__(self):
        self.static_vars = {}   # name -> (type, address)
        self.functions = {}     # name -> FunctionInfo
        self.structs = {}       # name -> StructInfo
        self.defines = {}       # name -> list[Token]
        self.macros = {}        # name -> (params: list[str], body: list[Token])
        self._next_static_addr = PROG_MEM_START_ADDR

    def type_size(self, var_type):
        if var_type in self.structs:
            return self.structs[var_type].size
        return var_size(var_type)

    def check_global_name_free(self, name):
        if name in KEYWORDS:
            raise MlvcSyntaxError(f"{name} is a reserved keyword!")
        if name in self.static_vars or name in self.functions:
            raise MlvcSyntaxError(f"Symbol {name} previously defined!")

    def check_struct_name_free(self, name):
        if name in KEYWORDS:
            raise MlvcSyntaxError(f"{name} is a reserved keyword!")
        if name in self.structs:
            raise MlvcSyntaxError(f"Symbol {name} previously defined!")

    def _reserve_static(self, name, size, address):
        self.check_global_name_free(name)

        if address is None:
            if self._next_static_addr + size > PROG_MEM_END_ADDR:
                raise MlvcMemoryError("Out of program memory!")
            address = self._next_static_addr
            self._next_static_addr += size

        return address

    def declare_static_var(self, name, var_type, address=None):
        address = self._reserve_static(name, self.type_size(var_type), address)
        self.static_vars[name] = (var_type, address)
        return address

    def declare_static_block(self, name, elem_type, count, address=None):
        address = self._reserve_static(name, self.type_size(elem_type) * count, address)
        self.static_vars[name] = (f"{elem_type}[]", address)
        return address

    def declare_data_block(self, name, elem_type):
        # A data block address is never known at compile time, it ends up wherever the assembler
        # places it in ROM, addressed by label. Storing None here makes resolve_static_address
        # correctly decide its not foldable.
        self.check_global_name_free(name)
        self.static_vars[name] = (f"{elem_type}[]", None)

    def declare_function(self, name, params, address=None):
        existing = self.functions.get(name)
        if existing is not None:
            if existing.defined:
                raise MlvcSyntaxError(f"Symbol {name} previously defined!")
            if [ptype for _, ptype in params] != [ptype for _, ptype in existing.params]:
                raise MlvcSyntaxError(f"{name} redefined with different parameters than its forward declaration!")
            existing.params = list(params)
            if address is not None:
                existing.address = address
            existing.defined = True
            return
        self.check_global_name_free(name)
        self.functions[name] = FunctionInfo(params=list(params), address=address, defined=True)

    def declare_function_signature(self, name, params, address=None):
        # A forward declaration
        # registers the signature so calls ahead of the real definition
        # typecheck, but declare_function must still supply the body later.
        self.check_global_name_free(name)
        self.functions[name] = FunctionInfo(params=list(params), address=address, defined=False)

    def declare_struct(self, name, field_list):
        self.check_struct_name_free(name)
        fields = {}
        offset = 0
        for field_name, field_type in field_list:
            fields[field_name] = (offset, field_type)
            offset += self.type_size(field_type)
        self.structs[name] = StructInfo(fields=fields, size=offset)
        return self.structs[name]

    def resolve_type(self, name, local_scope=None):
        if local_scope is not None and name in local_scope:
            return local_scope.var_offsets[name][1]
        if name in self.static_vars:
            return self.static_vars[name][0]
        return None

    def resolve_static_address(self, name):
        # None if name isn't a static var. Callers use this to test if an address is known at
        # compile time
        entry = self.static_vars.get(name)
        return entry[1] if entry is not None else None

    def is_read_only(self, name):
        # True only for a data block
        entry = self.static_vars.get(name)
        return entry is not None and entry[1] is None
