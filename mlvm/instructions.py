from mlvm.const import *
import random

INSTRUCTIONS = [None for _ in range(256)]

def instruction_from_name(name):
    return globals()[name]

def opcode_from_instruction(instruction):
    return INSTRUCTIONS.index(instruction)

### REGISTER LOADS ###

# Load next byte into the A register
INSTRUCTIONS[0x10] = LNA = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the A register
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data)
]

# Load next byte into the B register
INSTRUCTIONS[0x11] = LNB = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the B register
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

# Load next byte into the C register
INSTRUCTIONS[0x12] = LNC = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the C register
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data)
]

# Load next byte into the L register
INSTRUCTIONS[0x13] = LNL = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the L register
    lambda cpu: setattr(cpu, "reg_l", cpu.bus.data)
]

# Load next byte into the H register
INSTRUCTIONS[0x14] = LNH = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the H register
    lambda cpu: setattr(cpu, "reg_h", cpu.bus.data)
]

# Load next two bytes into the D register (little endian)
INSTRUCTIONS[0x15] = LND = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the L register, increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_l", cpu.bus.data), setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the H register
    lambda cpu: setattr(cpu, "reg_h", cpu.bus.data)
]

# Load next two bytes into the E register (little endian)
INSTRUCTIONS[0x16] = LNE = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the A register, increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_a", cpu.bus.data), setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load bus response into the B register
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]


### REGISTER ASSIGNMENTS ###

# Set A to B
INSTRUCTIONS[0x20] = SAB = [
    # Load the value of B into A
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_b)
]

# Set B to A
INSTRUCTIONS[0x21] = SBA = [
    # Load the value of A into B
    lambda cpu: setattr(cpu, "reg_b", cpu.reg_a)
]

# Set A to C
INSTRUCTIONS[0x22] = SAC = [
    # Load the value of C into A
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_c)
]

# Set C to A
INSTRUCTIONS[0x23] = SCA = [
    # Load the value of A into C
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a)
]

# Set B to C
INSTRUCTIONS[0x24] = SBC = [
    # Load the value of C into B
    lambda cpu: setattr(cpu, "reg_b", cpu.reg_c)
]

# Set C to B
INSTRUCTIONS[0x25] = SCB = [
    # Load the value of B into C
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_b)
]

# Set L to A
INSTRUCTIONS[0x26] = SLA = [
    # Load the value of A into L
    lambda cpu: setattr(cpu, "reg_l", cpu.reg_a)
]

# Set L to B
INSTRUCTIONS[0x27] = SLB = [
    # Load the value of B into L
    lambda cpu: setattr(cpu, "reg_l", cpu.reg_b)
]

# Set L to C
INSTRUCTIONS[0x28] = SLC = [
    # Load the value of C into L
    lambda cpu: setattr(cpu, "reg_l", cpu.reg_c)
]

# Set H to A
INSTRUCTIONS[0x29] = SHA = [
    # Load the value of A into H
    lambda cpu: setattr(cpu, "reg_h", cpu.reg_a)
]

# Set H to B
INSTRUCTIONS[0x2A] = SHB = [
    # Load the value of B into H
    lambda cpu: setattr(cpu, "reg_h", cpu.reg_b)
]

# Set H to C
INSTRUCTIONS[0x2B] = SHC = [
    # Load the value of C into H
    lambda cpu: setattr(cpu, "reg_h", cpu.reg_c)
]

# Set E to D
INSTRUCTIONS[0x2C] = SED = [
    # Load the value of L into A, load the value of H into B
    lambda cpu: (
        setattr(cpu, "reg_a", cpu.reg_l),
        setattr(cpu, "reg_b", cpu.reg_h)
    )
]

# Set D to E
INSTRUCTIONS[0x2D] = SDE = [
    # Load the value of A into L, load the value of B into H
    lambda cpu: (
        setattr(cpu, "reg_l", cpu.reg_a),
        setattr(cpu, "reg_h", cpu.reg_b)
    )
]

# Set A to S
INSTRUCTIONS[0x2E] = SAS = [
    # Load the value of S into A
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_s)
]


### REGISTER WRITES ###

# Write the A register to the address in D
INSTRUCTIONS[0x30] = WRA = [
    # Bus write A register at the D register
    lambda cpu: cpu.bus.write((cpu.reg_h << 8) | cpu.reg_l, cpu.reg_a),
    # Wait a clock for write to finish
    None
]

# Write the B register to the address in D
INSTRUCTIONS[0x31] = WRB = [
    # Bus write B register at the D register
    lambda cpu: cpu.bus.write((cpu.reg_h << 8) | cpu.reg_l, cpu.reg_b),
    # Wait a clock for write to finish
    None
]

# Write the C register to the address in D
INSTRUCTIONS[0x32] = WRC = [
    # Bus write C register at the D register
    lambda cpu: cpu.bus.write((cpu.reg_h << 8) | cpu.reg_l, cpu.reg_c),
    # Wait a clock for write to finish
    None
]

# Write the E register to the address in D
INSTRUCTIONS[0x33] = WRE = [
    # Bus write A register at the D register
    lambda cpu: cpu.bus.write(((cpu.reg_h << 8) | cpu.reg_l), cpu.reg_a),
    # Bus write B register at the D register plus one
    lambda cpu: cpu.bus.write((((cpu.reg_h << 8) | cpu.reg_l) + 1) & 0xFFFF, cpu.reg_b),
    # Wait a clock for write to finish
    None
]


### BUS READS ###

# Read the bus at the D register into the A register
INSTRUCTIONS[0x34] = RDA = [
    # Bus read at the D register
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    # Load bus data lines into the A register
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data)
]

# Read the bus at the D register into the B register
INSTRUCTIONS[0x35] = RDB = [
    # Bus read at the D register
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    # Load bus data lines into the B register
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

# Read the bus at the D register into the C register
INSTRUCTIONS[0x36] = RDC = [
    # Bus read at the D register
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    # Load bus data lines into the C register
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

# Read the bus at the D register into the E register
INSTRUCTIONS[0x37] = RDE = [
    # Bus read at the D register
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    # Load bus data lines into the A register, bus read at the D register plus one
    lambda cpu: (setattr(cpu, "reg_a", cpu.bus.data), cpu.bus.read(((cpu.reg_h << 8) | cpu.reg_l) + 1)),
    # Load bus data lines into the B register
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]


### OPERATORS ###

# Bitwise and, C = A & B
INSTRUCTIONS[0x40] = AND = [
    # Set the C register to A & B
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a & cpu.reg_b)
]


# Bitwise or, C = A | B
INSTRUCTIONS[0x41] = IOR = [
    # Set the C register to A | B
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a | cpu.reg_b)
]

# Bitwise xor, C = A ^ B
INSTRUCTIONS[0x42] = XOR = [
    # Set the C register to A ^ B
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a | cpu.reg_b)
]

# Bitwise not, C = ~A
INSTRUCTIONS[0x43] = NOT = [
    # Set the C register to ~A
    lambda cpu: setattr(cpu, "reg_c", ~cpu.reg_a)
]

# Addition, C = A + B, set the carry bit in the status register if overflowed
INSTRUCTIONS[0x44] = ADD = [
    # Set the C register to A + B, set the carry bit in the status register to (A + B > 0xFF)
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a + cpu.reg_b) & 0xFF),
        setattr(cpu, "reg_s", (cpu.reg_s | STATUS_CARRY) if (cpu.reg_a + cpu.reg_b) > 0xFF else (cpu.reg_s & ~STATUS_CARRY))
    )
]

# Subtraction, C = A - B, set the carry bit in the status register if overflowed
INSTRUCTIONS[0x45] = SUB = [
    # Set the C register to A - B, set the carry bit in the status register to (A - B > 0xFF)
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a + (~cpu.reg_b + 1) & 0xFF) & 0xFF),
        setattr(cpu, "reg_s", (cpu.reg_s | STATUS_CARRY) if (cpu.reg_a + (~cpu.reg_b + 1) & 0xFF) > 0xFF else (cpu.reg_s & ~STATUS_CARRY))
    )
]

# Multiplication, D = A * B, C = (A * B) & 0xFF
INSTRUCTIONS[0x46] = MUL = [
    # Set the C register to (A * B) & 0xFF, set the D register to A * B
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a * cpu.reg_b) & 0xFF),
        setattr(cpu, "reg_l", (cpu.reg_a * cpu.reg_b) & 0xFF),
        setattr(cpu, "reg_h", ((cpu.reg_a * cpu.reg_b) >> 8) & 0xFF)
    )
]

# Right bit shift, C = A >> B
INSTRUCTIONS[0x47] = RSS = [
    # Set the C register to A >> B
    lambda cpu: setattr(cpu, "reg_c", (cpu.reg_a >> cpu.reg_b) & 0xFF)
]

# Left bit shift, C = A << B
INSTRUCTIONS[0x48] = LSS = [
    # Set the C register to A << B
    lambda cpu: setattr(cpu, "reg_c", (cpu.reg_a << cpu.reg_b) & 0xFF)
]

# Logical and, C = A and B
INSTRUCTIONS[0x49] = ANL = [
    # Set the C register to A and B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a and cpu.reg_b))
]

# Modulo, C = A % B
INSTRUCTIONS[0x4A] = MOD = [
    # Set the C register to A % B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a % cpu.reg_b))
]

# Integer division, C = A // B
INSTRUCTIONS[0x4B] = DIV = [
    # Set the C register to A // b
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a // cpu.reg_b))
]


### COMPARISON OPERATORS ###

# Equals comparison, C = A == B
INSTRUCTIONS[0x50] = CMP = [
    # Set the C register to A == B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a == cpu.reg_b))
]

# Greater than or equal to, C = A >= B
INSTRUCTIONS[0x51] = GTE = [
    # Set the C register to A >= B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a >= cpu.reg_b))
]

# Less than or equal to, C = A <= B
INSTRUCTIONS[0x52] = LTE = [
    # Set the C register to A <= B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a <= cpu.reg_b))
]

# Greater than, C = A > B
INSTRUCTIONS[0x53] = GTC = [
    # Set the C register to A > B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a > cpu.reg_b))
]

# Less than, C = A < B
INSTRUCTIONS[0x54] = LTC = [
    # Set the C register to A < B
    lambda cpu: setattr(cpu, "reg_c", int(cpu.reg_a < cpu.reg_b))
]


### STACK OPERATIONS ###

# Push the C register to the stack
INSTRUCTIONS[0x60] = PSH = [
    # Bus write C register at the T register, increment the T register
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_c),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    # Wait a clock for write to finish
    None
]

# Pull the top of the stack into the C register
INSTRUCTIONS[0x61] = PUL = [
    # Decrement the T register, bus read the at the T register
    lambda cpu: (
        (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...,
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t)
    ),
    # Load data lines into the C register
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data)
]

# Jump to subroutine
INSTRUCTIONS[0x62] = SRT = [
    # Bus write low byte of the program counter at the T register, increment the T register
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    # Bus write high byte of the program counter at the T register, increment the T register
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    # Set the program counter to the D register
    lambda cpu: setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)
]

INSTRUCTIONS[0x63] = SIA = [
    # Bus write low byte of the program counter at the T register if A, increment the T register if A
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ) if cpu.reg_a else ...,
    # Bus write high byte of the program counter at the T register if A, increment the T register if A
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    )  if cpu.reg_a else ...,
    # Set the program counter to the D register if A
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)) if cpu.reg_a else ...
]

INSTRUCTIONS[0x64] = SIB = [
    # Bus write low byte of the program counter at the T register if B, increment the T register if B
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ) if cpu.reg_b else ...,
    # Bus write high byte of the program counter at the T register if B, increment the T register if B
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    )  if cpu.reg_b else ...,
    # Set the program counter to the D register if B
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)) if cpu.reg_b else ...
]

INSTRUCTIONS[0x65] = SIC = [
    # Bus write low byte of the program counter at the T register if C, increment the T register if C
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ) if cpu.reg_c else ...,
    # Bus write high byte of the program counter at the T register if C, increment the T register if C
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    )  if cpu.reg_c else ...,
    # Set the program counter to the D register if C
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)) if cpu.reg_c else ...
]

# Jump to subroutine with immediate addressing
INSTRUCTIONS[0x66] = SRI = [
    # Increment program counter, bus read at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load data lines into the L register, increment the program counter, bus read at program counter
    lambda cpu: (setattr(cpu, "reg_l", cpu.bus.data), setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load data lines into the H register, bus write low byte of the program counter at the T register, increment the T register
    lambda cpu: (
        setattr(cpu, "reg_h", cpu.bus.data),
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    # Bbus write high byte of the program counter at the T register, increment the T register
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    # Set the program counter to the D register
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF))
]

# Return from subroutine
INSTRUCTIONS[0x67] = RET = [
    # Decrement T register, bus read at T register
    lambda cpu: (
        (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...,
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t)
    ),
    # Load data lines into the H register, decrement T register, bus read at T register
    lambda cpu: (
        setattr(cpu, "reg_h", cpu.bus.data),
        (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...,
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t)
    ),
    # Load datalines into the L register, set the program counter to the D register
    lambda cpu: (
        setattr(cpu, "reg_l", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_l | (cpu.reg_h << 8)) & 0xFFFF)
    )
]


### JUMP INSTRUCTIONS ###

# Jump to the D register
INSTRUCTIONS[0x70] = JMP = [
    # Load the D register into the program counter
    lambda cpu: setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)
]

# Jump to the D register if A
INSTRUCTIONS[0x71] = JIA = [
    # Load the D register into the program counter if A
    lambda cpu: JMP[0](cpu) if cpu.reg_a else ...
]

# Jump to the D register if B
INSTRUCTIONS[0x72] = JIB = [
    # Load the D register into the program counter if B
    lambda cpu: JMP[0](cpu) if cpu.reg_b else ...
]

# Jump to the D register if C
INSTRUCTIONS[0x73] = JIC = [
    # Load the D register into the program counter if C
    lambda cpu: JMP[0](cpu) if cpu.reg_c else ...
]

# Jump to the D register if not A
INSTRUCTIONS[0x74] = JIX = [
    # Load the D register into the program counter if not A
    lambda cpu: JMP[0](cpu) if not cpu.reg_a else ...
]

# Jump to the D register if not B
INSTRUCTIONS[0x75] = JIY = [
    # Load the D register into the program counter if not B
    lambda cpu: JMP[0](cpu) if not cpu.reg_b else ...
]

# Jump to the D register if not C
INSTRUCTIONS[0x76] = JIZ = [
    # Load the D register into the program counter if not C
    lambda cpu: JMP[0](cpu) if not cpu.reg_c else ...
]

# Jump to the D register if the carry bit is set
INSTRUCTIONS[0x77] = JSC = [
    # Load the D register into the program counter if the carry bit is set
    lambda cpu: JMP[0](cpu) if (cpu.reg_s & STATUS_CARRY) else ...
]

# Jump to the address in the next two bytes
INSTRUCTIONS[0x78] = JMI = [
    # Increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load data lines into the L register, increment program counter, read bus at program counter
    lambda cpu: (setattr(cpu, "reg_l", cpu.bus.data), setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    # Load data lines into the H register, load the D register into the program counter
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF))
]

INSTRUCTIONS[0x79] = JAI = [
    # Increment program counter, read bus at program counter
    JMI[0],
    # Load data lines into the L register, increment program counter, read bus at program counter
    JMI[1],
    # Load data lines into the H register, load the D register into the program counter if A
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF) if cpu.reg_a else ...)
]

INSTRUCTIONS[0x7A] = JBI = [
    # Increment program counter, read bus at program counter
    JMI[0],
    # Load data lines into the L register, increment program counter, read bus at program counter
    JMI[1],
    # Load data lines into the H register, load the D register into the program counter if B
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF) if cpu.reg_b else ...)
]

INSTRUCTIONS[0x7B] = JCI = [
    # Increment program counter, read bus at program counter
    JMI[0],
    # Load data lines into the L register, increment program counter, read bus at program counter
    JMI[1],
    # Load data lines into the H register, load the D register into the program counter if C
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF) if cpu.reg_c else ...)
]

INSTRUCTIONS[0x7C] = JXI = [
    # Increment program counter, read bus at program counter
    JMI[0],
    # Load data lines into the L register, increment program counter, read bus at program counter
    JMI[1],
    # Load data lines into the H register, load the D register into the program counter if not A
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF) if not cpu.reg_a else ...)
]

INSTRUCTIONS[0x7D] = JYI = [
    # Increment program counter, read bus at program counter
    JMI[0],
    # Load data lines into the L register, increment program counter, read bus at program counter
    JMI[1],
    # Load data lines into the H register, load the D register into the program counter if not B
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF) if not cpu.reg_b else ...)
]

INSTRUCTIONS[0x7E] = JZI = [
    # Increment program counter, read bus at program counter
    JMI[0],
    # Load data lines into the L register, increment program counter, read bus at program counter
    JMI[1],
    # Load data lines into the H register, load the D register into the program counter if C
    lambda cpu: (setattr(cpu, "reg_h", cpu.bus.data), setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF) if not cpu.reg_c else ...)
]


### UTILITY ###

# Random number generator, A = randint(0, 255)
INSTRUCTIONS[0x80] = RND = [
    # Load a random number from 0 to 255 into the A register
    lambda cpu: setattr(cpu, "reg_a", random.randint(0, 255))
]


### SYSTEM CONTROL ###

# Halt, stop processing
INSTRUCTIONS[0xE0] = HLT = [
    # Halt the cpu
    lambda cpu: (print("HALT"), setattr(cpu, "reg_s", cpu.reg_s | STATUS_HALT))
]


### DEBUG INSTRUCTIONS ###

# Debug A register
INSTRUCTIONS[0xF0] = DLA = [
    # Print A register
    lambda cpu: print("A:", cpu.reg_a)
]

# Debug B register
INSTRUCTIONS[0xF1] = DLB = [
    # Print B register
    lambda cpu: print("B:", cpu.reg_b)
]

# Debug C register
INSTRUCTIONS[0xF2] = DLC = [
    # Print C register
    lambda cpu: print("C:", cpu.reg_c)
]
