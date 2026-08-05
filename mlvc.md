# MLVC Language Reference


## Comments

```mlvc
/* block comment, can span
   multiple lines */
```

No line comments, `//` has no meaning.

## Types

| Type | Size | Notes |
|---|---|---|
| `u8` | 1 byte | unsigned |
| `u16` | 2 bytes | unsigned |
| `i8` | 1 byte | signed |
| `i16` | 2 bytes | signed |
| `[type]` | 2 bytes | pointer to `type`
| struct name | sum of fields | see Structs |

## Literals

### Decimal

```mlvc
42
```

### Hexadecimal

```mlvc
0x2A
```

### Binary

```mlvc
0b101010
```

### Negative

```mlvc
-5
```

### Char

```mlvc
'a'
```

Becomes its byte value at compile time. `'a'` and `97` are the same value.

### String

```mlvc
"hi"
```

Null terminated. Compiles to a hidden ROM data block, and the literal itself is replaced with that block's address.

### Escapes

```mlvc
'\n'   /* 10, newline */
'\r'   /* 13, carriage return */
'\0'   /* 0, null */
'\\'   /* backslash */
'\"'   /* double quote */
'\''   /* single quote */
```

Valid inside both char and string literals.

## Operators

```
&& == != >= <= > < | ^ & << >> + - * / % ~ - (unary)
```

Listed lowest to highest precedence.

```mlvc
(a + b) * 2
```

Parentheses group as usual and override precedence.

There is no `||`. `&&` is the only logical operator, and it does not short circuit. Both sides are always evaluated, even when a side is a `?fn()` call with side effects.

## Variables

### Basic declaration

```
var u8 counter;
```

### Pinned to a fixed address

```
var u16 status_reg @ 0x6000;
```

### Multiple at once

```
var u8 a b c;
```

Space separated, declares three variables sharing the one type.

### Local vs static

Outside a function, `var` is always static. Inside a function, `var` declares a local, and every
local declaration must come before any other statement in the function:

```mlvc
fn example {
    var u8 a;
    set a = 1;
    var u8 b;   /* error */
}
```

Locals also can't be pinned to an address, and can't be declared inside a nested `if`/`while`
block, only directly in the function's own body. `array` locals follow these same two rules.

## Blocks

```mlvc
array u8 32 buffer;
```

32 bytes, uninitialized, zeroed at boot.

### Array of structs

```mlvc
array point_t 4 points;
```

### Pinned to a fixed address

```mlvc
array u8 16 fixed_buf @ 0x1000;
```

### Naming

A block's name refers to the block itself, never a value. `@buffer` gives its address. A bare `buffer` used as a value anywhere is a compile error.

## Data blocks

ROM resident, initialized at compile time, read only.

### String

```mlvc
data u8 message "Hello!";
```

Null terminated.

### Explicit values

```mlvc
data u8 table { 1, 2, 3, 4 };
```

Element type must be a scalar (`u8`/`u16`/`i8`/`i16`), never a struct or pointer.

## Structs

### Declaration

```mlvc
struct point_t {
    u8 x;
    u8 y;
};
```

Fields must be scalar or pointer types. A struct can never embed another struct by value, only a
pointer to one.

### Plain struct variable

```mlvc
var point_t pt;
set pt.x = 1;
```

### Pointer to struct

```mlvc
var [point_t] pp;
set pp = @pt;
set [pp].y = 2;
```

Field access through a struct pointer always uses `[pp].field`, never `pp.field`.

### Array of structs, write

```mlvc
array point_t 4 points;
set points<0>.x = 5;
set points<counter>.y = 9;
```

### Array of structs, read

```mlvc
set someval = points<0>.x;
```

### Array field

```mlvc
struct inode_t {
    u8 type;
    array u16 30 indirect;
};

var inode_t node;
set node.indirect<3> = 500;
set someval = node.indirect<3>;
```


## Pointers

### Declare and assign

```mlvc
var [u8] p;
set p = @buffer;
```

### Write through a pointer

```mlvc
set [p] = 42;
```

### Read through a pointer

```mlvc
set counter = [p];
```

A `[expr]` dereference on a single named pointer variable infers its width from the pointer's own declared type, no explicit type needed.

### Computed address, write

```mlvc
set [u16 @buffer + 4] = 0xBEEF;
```

A computed, multi-token address needs an explicit `[TYPE expr]`. This is also a way to reach a specific element of a scalar block: `@buffer + offset`.

### Computed address, read

```mlvc
set counter = [u16 @buffer + 4];
```

### Computed address, read with default type

```mlvc
set counter = [@buffer + 4];
```

On the read side only, leaving the type out defaults to `u8`.

## Functions

### With parameters

```mlvc
fn add(u8 a, u8 b) {
    return a + b;
}
```

### No parameters

```mlvc
fn no_args {
    return;
}
```

Parentheses are optional when there are zero parameters.

### Pinned to a fixed address

```mlvc
fn isr_handler @ 0xFFE0 {
    asm { HLT }
    rti;
}
```

Useful for interrupt vectors and other fixed entry points.

### Forward declaration

```mlvc
fn is_even(u16 n);

fn is_odd(u16 n) {
    if n == 0 {
        return 0;
    }
    return ?is_even(n - 1);
}

fn is_even(u16 n) {
    if n == 0 {
        return 1;
    }
    return ?is_odd(n - 1);
}
```

A signature ending in `;` instead of a braced block forward declares the function so code can call it without defining it yet. The real definition (matching parameter types) must appear later on.

### Return values

```mlvc
return;
return counter;
```

`return;` with no value leaves the result register untouched. `return expr;` leaves the result in
it.

## Program entry

```mlvc
begin

set counter = 0;
while 1 { }
```

`begin` marks where execution starts. Everything before it is declarations everything after it runs at boot.

## Statements

### set

```mlvc
set counter = 0;
```

### if

```mlvc
if counter == 10 {
    set counter = 0;
}
```

### if / else

```mlvc
if counter == 10 {
    set counter = 0;
} else {
    set counter = 1;
}
```

### if / else if / else

```mlvc
if counter == 10 {
    set counter = 0;
} else if counter > 5 {
    set counter = 5;
} else {
    set counter = 1;
}
```

`if` has no fallthrough between branches

### while

```mlvc
while counter < 10 {
    incr counter;
}
```

### incr / decr

```mlvc
incr counter;
decr counter;
```

Target must be a scalar or pointer variable.

### call, with arguments

```mlvc
call add(1, 2);
```

### call, no arguments

```mlvc
call no_args;
call no_args();
```

Both forms are equivalent, parentheses are optional only when there are zero arguments.

### asm block

```mlvc
asm {
    CLI
    LIA 0x100
}
```

Raw MLVS instructions, spliced directly into the generated assembly. `@name` inside an `asm` block only resolves static vars, blocks, and functions, never a local or a parameter.

### rti

```mlvc
rti;
```

Return from interrupt.

### svi / ldi

```mlvc
svi expr;
ldi expr;
```

Kernel only. `svi` saves the pending interrupt frame to the address `expr` and `ldi` loads it back from `expr`, replacing the frame that the next `rti` will resume into.

## Expressions

### Function call as an operand

```mlvc
set counter = ?add(1, 2);
```

Parentheses are required even for zero arguments: `?no_args()`

### Address of

```mlvc
set p = @counter;
```

Works on a var, block, function, or data block.

### Arithmetic

```mlvc
counter + 1
(a + b) * 2
```

### String or char literal inline

```mlvc
set p = "hi";
```

Same hidden-data-block behavior as a string used in a `data` declaration; usable anywhere an
expression is, not just there.

## Preprocessor

### define

```mlvc
define PI_APPROX 3;
```

```mlvc
#PI_APPROX
```

Plain token substitution. Expands to `3`.

### macro

```mlvc
macro SQUARE(X) {
    ((#X) * (#X))
}
```

```mlvc
#SQUARE(3)
```

Expands to `((3) * (3))`. A macro body can span multiple statements, and can itself call other macros.

Both `define` and `macro` are pure textual substitution, with no auto-parenthesization: if precedence matters, parenthesize the body yourself, the way `SQUARE` does above.

### include

```mlvc
include mlib/graphics.mlvc;
```

Internally includes the lines of the included file in the current file at the include point. Re-including the same file that was already included or transitively included is a no-op.
