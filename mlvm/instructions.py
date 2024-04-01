from mlvm.const import *
import random

INSTRUCTIONS = [None for _ in range(256)]

# Load next byte into register (r = bus[pc + 1])

INSTRUCTIONS[0x10] = LNA = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data)
]

INSTRUCTIONS[0x11] = LNB = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

INSTRUCTIONS[0x12] = LNC = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_c", cpu.bus.data)
]

INSTRUCTIONS[0x13] = LNL = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_l", cpu.bus.data)
]

INSTRUCTIONS[0x14] = LNH = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_h", cpu.bus.data)
]

INSTRUCTIONS[0x15] = LND = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: (setattr(cpu, "reg_l", cpu.bus.data), setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_h", cpu.bus.data)
]

INSTRUCTIONS[0x16] = LNE = [
    lambda cpu: (setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: (setattr(cpu, "reg_a", cpu.bus.data), setattr(cpu, "reg_p", (cpu.reg_p + 1) & 0xFFFF), cpu.bus.read(cpu.reg_p)),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

# Assign a register to another (r1 = r2)

INSTRUCTIONS[0x20] = SAB = [
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_b)
]

INSTRUCTIONS[0x21] = SBA = [
    lambda cpu: setattr(cpu, "reg_b", cpu.reg_a)
]

INSTRUCTIONS[0x22] = SAC = [
    lambda cpu: setattr(cpu, "reg_a", cpu.reg_c)
]

INSTRUCTIONS[0x23] = SCA = [
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a)
]

INSTRUCTIONS[0x24] = SBC = [
    lambda cpu: setattr(cpu, "reg_b", cpu.reg_c)
]

INSTRUCTIONS[0x25] = SCB = [
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_b)
]

INSTRUCTIONS[0x26] = SLA = [
    lambda cpu: setattr(cpu, "reg_l", cpu.reg_a)
]

INSTRUCTIONS[0x27] = SLB = [
    lambda cpu: setattr(cpu, "reg_l", cpu.reg_b)
]

INSTRUCTIONS[0x28] = SLC = [
    lambda cpu: setattr(cpu, "reg_l", cpu.reg_c)
]

INSTRUCTIONS[0x29] = SHA = [
    lambda cpu: setattr(cpu, "reg_h", cpu.reg_a)
]

INSTRUCTIONS[0x2A] = SHB = [
    lambda cpu: setattr(cpu, "reg_h", cpu.reg_b)
]

INSTRUCTIONS[0x2B] = SHC = [
    lambda cpu: setattr(cpu, "reg_h", cpu.reg_c)
]

INSTRUCTIONS[0x2C] = SED = [
    lambda cpu: (
        setattr(cpu, "reg_a", cpu.reg_l),
        setattr(cpu, "reg_b", cpu.reg_h)
    )
]

INSTRUCTIONS[0x2D] = SDE = [
    lambda cpu: (
        setattr(cpu, "reg_l", cpu.reg_a),
        setattr(cpu, "reg_h", cpu.reg_b)
    )
]

# Write to bus (bus[h,l] = r)

INSTRUCTIONS[0x30] = WRA = [
    lambda cpu: cpu.bus.write((cpu.reg_h << 8) | cpu.reg_l, cpu.reg_a),
    None
]

INSTRUCTIONS[0x31] = WRB = [
    lambda cpu: cpu.bus.write((cpu.reg_h << 8) | cpu.reg_l, cpu.reg_b),
    None
]

INSTRUCTIONS[0x32] = WRC = [
    lambda cpu: cpu.bus.write((cpu.reg_h << 8) | cpu.reg_l, cpu.reg_c),
    None
]

INSTRUCTIONS[0x33] = WRE = [
    lambda cpu: cpu.bus.write(((cpu.reg_h << 8) | cpu.reg_l), cpu.reg_a),
    lambda cpu: cpu.bus.write((((cpu.reg_h << 8) | cpu.reg_l) + 1) & 0xFFFF, cpu.reg_b),
    None
]


# Read from bus (r = bus[h,l])

INSTRUCTIONS[0x34] = RDA = [
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data)
]

INSTRUCTIONS[0x35] = RDB = [
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

INSTRUCTIONS[0x36] = RDC = [
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

INSTRUCTIONS[0x37] = RDE = [
    lambda cpu: cpu.bus.read((cpu.reg_h << 8) | cpu.reg_l),
    lambda cpu: (setattr(cpu, "reg_a", cpu.bus.data), cpu.bus.read(((cpu.reg_h << 8) | cpu.reg_l) + 1)),
    lambda cpu: setattr(cpu, "reg_b", cpu.bus.data)
]

# c = a & b

INSTRUCTIONS[0x40] = AND = [
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a & cpu.reg_b)
]


# c = a | b

INSTRUCTIONS[0x41] = IOR = [
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a | cpu.reg_b)
]


# c = a ^ b

INSTRUCTIONS[0x42] = XOR = [
    lambda cpu: setattr(cpu, "reg_c", cpu.reg_a | cpu.reg_b)
]


# c = ~a

INSTRUCTIONS[0x43] = NOT = [
    lambda cpu: setattr(cpu, "reg_c", ~cpu.reg_a)
]


# c = a + b

INSTRUCTIONS[0x44] = ADD = [
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a + cpu.reg_b) & 0xFF),
        setattr(cpu, "reg_s", (cpu.reg_s | STATUS_CARRY) if (cpu.reg_a + cpu.reg_b) > 0xFF else (cpu.reg_s & ~STATUS_CARRY))
    )
]

# c = a + b

INSTRUCTIONS[0x45] = SUB = [
    lambda cpu: (
        setattr(cpu, "reg_c", (cpu.reg_a + (~cpu.reg_b + 1) & 0xFF) & 0xFF),
        setattr(cpu, "reg_s", (cpu.reg_s | STATUS_CARRY) if (cpu.reg_a + (~cpu.reg_b + 1) & 0xFF) > 0xFF else (cpu.reg_s & ~STATUS_CARRY))
    )
]


# h,l = a * b

INSTRUCTIONS[0x46] = MUL = [
    lambda cpu: (
        setattr(cpu, "reg_l", (cpu.reg_a * cpu.reg_b) & 0xFF),
        setattr(cpu, "reg_h", ((cpu.reg_a * cpu.reg_b) >> 8) & 0xFF)
    )
]


# a = a >> 1

INSTRUCTIONS[0x47] = RSA = [
    lambda cpu: setattr(cpu, "reg_a", (cpu.reg_a >> 1) & 0xFF)
]


# a = a << 1

INSTRUCTIONS[0x48] = LSA = [
    lambda cpu: setattr(cpu, "reg_a", (cpu.reg_a << 1) & 0xFF)
]

# a == b

INSTRUCTIONS[0x49] = CMP = [
    lambda cpu: setattr(cpu, "reg_s", (cpu.reg_s | STATUS_CARRY) if cpu.reg_a == cpu.reg_b else (cpu.reg_s & ~STATUS_CARRY))
]

# Stack operations and jumps

INSTRUCTIONS[0x50] = PSH = [
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_a),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    None
]

INSTRUCTIONS[0x51] = PUL = [
    lambda cpu: (
        (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...,
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t)
    ),
    lambda cpu: setattr(cpu, "reg_a", cpu.bus.data)
]

INSTRUCTIONS[0x52] = SRT = [
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ),
    lambda cpu: setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)
]

INSTRUCTIONS[0x53] = SRC = [
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, cpu.reg_p & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    ) if cpu.reg_s & STATUS_CARRY else ...,
    lambda cpu: (
        (print("STACK OVERFLOW"), exit(ERR_STACK_OVERFLOW)) if cpu.reg_t > STACK_POINTER_MAX else ...,
        cpu.bus.write(STACK_START_ADDR + cpu.reg_t, (cpu.reg_p >> 8) & 0xFF),
        setattr(cpu, "reg_t", (cpu.reg_t + 1) & 0xFFFF)
    )  if cpu.reg_s & STATUS_CARRY else ...,
    lambda cpu: (setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)) if cpu.reg_s & STATUS_CARRY else ...
]


INSTRUCTIONS[0x54] = RET = [
    lambda cpu: (
        (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...,
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t)
    ),
    lambda cpu: (
        setattr(cpu, "reg_h", cpu.bus.data),
        (print("STACK UNDERFLOW"), exit(ERR_STACK_UNDERFLOW)) if cpu.reg_t == 0 else ...,
        setattr(cpu, "reg_t", (cpu.reg_t - 1) & 0xFFFF),
        cpu.bus.read(STACK_START_ADDR + cpu.reg_t)
    ),
    lambda cpu: (
        setattr(cpu, "reg_l", cpu.bus.data),
        setattr(cpu, "reg_p", (cpu.reg_l | (cpu.reg_h << 8)) & 0xFFFF)
    )
]

INSTRUCTIONS[0x55] = JMP = [
    lambda cpu: setattr(cpu, "reg_p", ((cpu.reg_l | (cpu.reg_h << 8)) - 1) & 0xFFFF)
]

INSTRUCTIONS[0x56] = JIA = [
    lambda cpu: JMP[0](cpu) if cpu.reg_a else ...
]

INSTRUCTIONS[0x57] = JIB = [
    lambda cpu: JMP[0](cpu) if cpu.reg_b else ...
]

INSTRUCTIONS[0x58] = JIC = [
    lambda cpu: JMP[0](cpu) if cpu.reg_c else ...
]

INSTRUCTIONS[0x59] = JNA = [
    lambda cpu: JMP[0](cpu) if not cpu.reg_a else ...
]

INSTRUCTIONS[0x5A] = JNB = [
    lambda cpu: JMP[0](cpu) if not cpu.reg_b else ...
]

INSTRUCTIONS[0x5B] = JNC = [
    lambda cpu: JMP[0](cpu) if not cpu.reg_c else ...
]

INSTRUCTIONS[0x5C] = JSC = [
    lambda cpu: JMP[0](cpu) if (cpu.reg_s & STATUS_CARRY) else ...
]

# Random util
INSTRUCTIONS[0x60] = RND = [
    lambda cpu: setattr(cpu, "reg_a", random.randint(0, 255))
]

# System control

INSTRUCTIONS[0xE0] = HLT = [
    lambda cpu: (print("HALT"), exit(ERR_HALT))
]


# Debug

INSTRUCTIONS[0xF0] = DLA = [
    lambda cpu: print("DEBUG LOG:", cpu.reg_a)
]
